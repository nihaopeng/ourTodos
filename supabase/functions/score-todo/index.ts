import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const OPENAI_API_KEY = Deno.env.get('OPENAI_API_KEY');

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface ScoreRequest {
  title: string;
  description: string;
  criteria: {
    importance?: number;
    urgency?: number;
    complexity?: number;
    impact?: number;
    [key: string]: number | undefined;
  };
}

serve(async (req) => {
  // 处理CORS预检请求
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const { title, description, criteria }: ScoreRequest = await req.json();

    if (!title || !description) {
      return new Response(
        JSON.stringify({ error: '标题和描述不能为空' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    if (!OPENAI_API_KEY) {
      console.error('OPENAI_API_KEY未配置');
      // 返回默认评分
      return new Response(
        JSON.stringify({
          score: 50,
          reasoning: '使用默认评分',
          breakdown: criteria,
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // 构建评分标准说明
    const criteriaText = Object.entries(criteria)
      .map(([key, value]) => `${key}: ${(value || 0) * 100}%`)
      .join(', ');

    // 调用OpenAI API
    const openaiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: `你是一个待办事项评分助手。根据用户提供的待办事项标题和描述，以及评分标准（${criteriaText}），给出一个0-100分的评分。
评分应该综合考虑：
- 重要性(importance)：任务对目标的重要程度
- 紧急性(urgency)：任务的时间敏感度
- 复杂性(complexity)：任务的难度和所需时间
- 影响力(impact)：完成任务后的影响范围

请以JSON格式返回评分结果，格式如下：
{
  "score": 75,
  "reasoning": "简短的评分理由",
  "breakdown": {
    "importance": 80,
    "urgency": 70,
    "complexity": 75,
    "impact": 75
  }
}`,
          },
          {
            role: 'user',
            content: `标题：${title}\n描述：${description}`,
          },
        ],
        temperature: 0.7,
        max_tokens: 500,
      }),
    });

    if (!openaiResponse.ok) {
      const errorText = await openaiResponse.text();
      console.error('OpenAI API错误:', errorText);
      throw new Error('AI评分失败');
    }

    const openaiData = await openaiResponse.json();
    const content = openaiData.choices[0]?.message?.content;

    if (!content) {
      throw new Error('AI返回内容为空');
    }

    // 解析AI返回的JSON
    let result;
    try {
      // 尝试提取JSON内容（可能包含在markdown代码块中）
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        result = JSON.parse(jsonMatch[0]);
      } else {
        result = JSON.parse(content);
      }
    } catch (parseError) {
      console.error('解析AI返回内容失败:', content);
      throw new Error('解析评分结果失败');
    }

    // 确保评分在0-100范围内
    const score = Math.max(0, Math.min(100, Math.round(result.score || 50)));

    return new Response(
      JSON.stringify({
        score,
        reasoning: result.reasoning || '基于AI分析的评分',
        breakdown: result.breakdown || criteria,
      }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('评分失败:', error);
    
    // 返回默认评分而不是错误
    return new Response(
      JSON.stringify({
        score: 50,
        reasoning: '使用默认评分',
        breakdown: {},
      }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});
