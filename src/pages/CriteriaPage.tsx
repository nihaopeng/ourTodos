import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import MainLayout from '@/components/layouts/MainLayout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Plus, Scale, Star, Pencil, Trash2 } from 'lucide-react';
import { getScoringCriteria, deleteScoringCriteria } from '@/db/api';
import type { ScoringCriteria } from '@/types/types';
import { useToast } from '@/hooks/use-toast';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import AddCriteriaDialog from '@/components/AddCriteriaDialog';
import EditCriteriaDialog from '@/components/EditCriteriaDialog';

export default function CriteriaPage() {
  const { user, profile } = useAuth();
  const { toast } = useToast();
  const [criteria, setCriteria] = useState<ScoringCriteria[]>([]);
  const [loading, setLoading] = useState(true);
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedCriteria, setSelectedCriteria] = useState<ScoringCriteria | null>(null);

  const isAdmin = profile?.role === 'admin';

  useEffect(() => {
    loadCriteria();
  }, [user]);

  const loadCriteria = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const data = await getScoringCriteria(user.id);
      setCriteria(data);
    } catch (error) {
      console.error('加载评分标准失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!selectedCriteria) return;

    try {
      await deleteScoringCriteria(selectedCriteria.id);
      toast({
        title: '删除成功',
        description: '评分标准已删除',
      });
      loadCriteria();
    } catch (error) {
      console.error('删除评分标准失败:', error);
      toast({
        title: '错误',
        description: '删除评分标准失败，请重试',
        variant: 'destructive',
      });
    } finally {
      setDeleteDialogOpen(false);
      setSelectedCriteria(null);
    }
  };

  const getCriteriaWeights = (criteriaJson: ScoringCriteria['criteria_json']) => {
    return Object.entries(criteriaJson)
      .filter(([_, value]) => value !== undefined)
      .map(([key, value]) => ({
        key,
        label: getCriteriaLabel(key),
        weight: Math.round((value || 0) * 100),
      }));
  };

  const getCriteriaLabel = (key: string) => {
    const labels: Record<string, string> = {
      importance: '重要性',
      urgency: '紧急性',
      complexity: '复杂性',
      impact: '影响力',
    };
    return labels[key] || key;
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* 页面标题 */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <img src="/images/brain.png" alt="AI评分" className="w-12 h-12" />
              <h1 className="text-3xl font-bold gradient-text">评分标准管理</h1>
            </div>
            <p className="text-muted-foreground">
              {isAdmin 
                ? '自定义AI评分标准，让评分更符合您的需求' 
                : '查看AI评分标准，了解任务评分规则'
              }
            </p>
          </div>
          {isAdmin && (
            <Button onClick={() => setAddDialogOpen(true)} className="gap-2">
              <Plus className="w-4 h-4" />
              添加标准
            </Button>
          )}
        </div>

        {/* 非管理员提示 */}
        {!isAdmin && (
          <Card className="border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                  <Scale className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">仅管理员可编辑</h3>
                  <p className="text-sm text-muted-foreground">
                    评分标准由管理员统一管理，以确保评分的一致性和公平性。如需修改评分标准，请联系管理员。
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* 评分标准列表 */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {loading ? (
            <>
              {[...Array(3)].map((_, i) => (
                <Card key={i}>
                  <CardHeader>
                    <Skeleton className="h-6 w-3/4 mb-2 bg-muted" />
                    <Skeleton className="h-4 w-1/2 bg-muted" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-20 w-full bg-muted" />
                  </CardContent>
                </Card>
              ))}
            </>
          ) : criteria.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="text-center py-12">
                <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                  <Scale className="w-8 h-8 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-medium mb-2">暂无评分标准</h3>
                <p className="text-muted-foreground mb-4">
                  {isAdmin 
                    ? '创建您的第一个评分标准，自定义AI评分规则' 
                    : '管理员尚未创建评分标准，请联系管理员添加'
                  }
                </p>
                {isAdmin && (
                  <Button onClick={() => setAddDialogOpen(true)} className="gap-2">
                    <Plus className="w-4 h-4" />
                    添加标准
                  </Button>
                )}
              </CardContent>
            </Card>
          ) : (
            criteria.map((item) => (
              <Card key={item.id} className="relative group">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="flex items-center gap-2">
                        {item.name}
                        {item.is_default && (
                          <Badge variant="secondary" className="text-xs">
                            <Star className="w-3 h-3 mr-1" />
                            默认
                          </Badge>
                        )}
                      </CardTitle>
                      <CardDescription className="mt-1">
                        {getCriteriaWeights(item.criteria_json).length} 个评分维度
                      </CardDescription>
                    </div>
                    {isAdmin && (
                      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => {
                            setSelectedCriteria(item);
                            setEditDialogOpen(true);
                          }}
                        >
                          <Pencil className="w-4 h-4" />
                        </Button>
                        {!item.is_default && (
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => {
                              setSelectedCriteria(item);
                              setDeleteDialogOpen(true);
                            }}
                          >
                            <Trash2 className="w-4 h-4 text-destructive" />
                          </Button>
                        )}
                      </div>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {getCriteriaWeights(item.criteria_json).map((weight) => (
                      <div key={weight.key}>
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-muted-foreground">{weight.label}</span>
                          <span className="font-medium">{weight.weight}%</span>
                        </div>
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full gradient-primary transition-all"
                            style={{ width: `${weight.weight}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* 说明卡片 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Scale className="w-5 h-5" />
              评分标准说明
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">什么是评分标准？</h4>
              <p className="text-sm text-muted-foreground">
                评分标准定义了AI如何评估您的待办事项。通过调整不同维度的权重，您可以让AI更关注某些方面。
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-2">评分维度说明</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <strong>重要性</strong>：任务对目标的重要程度</li>
                <li>• <strong>紧急性</strong>：任务的时间敏感度</li>
                <li>• <strong>复杂性</strong>：任务的难度和所需时间</li>
                <li>• <strong>影响力</strong>：完成任务后的影响范围</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">默认标准</h4>
              <p className="text-sm text-muted-foreground">
                标记为"默认"的评分标准将在创建新待办事项时自动使用。您可以在编辑时设置默认标准。
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {isAdmin && (
        <>
          <AddCriteriaDialog
            open={addDialogOpen}
            onOpenChange={setAddDialogOpen}
            onSuccess={loadCriteria}
          />

          {selectedCriteria && (
            <EditCriteriaDialog
              open={editDialogOpen}
              onOpenChange={setEditDialogOpen}
              criteria={selectedCriteria}
              onSuccess={loadCriteria}
            />
          )}

          <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>确认删除</AlertDialogTitle>
                <AlertDialogDescription>
                  确定要删除评分标准"{selectedCriteria?.name}"吗？此操作无法撤销。
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>取消</AlertDialogCancel>
                <AlertDialogAction onClick={handleDelete}>删除</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </>
      )}
    </MainLayout>
  );
}
