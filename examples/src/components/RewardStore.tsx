import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ShoppingCart, Gift, Star } from "lucide-react";
import { useState } from "react";

export interface Reward {
  id: string;
  name: string;
  description: string;
  cost: number;
  category: "玩具" | "零食" | "活动" | "特权";
  available: boolean;
  icon: string;
  popularity?: number;
}

interface RewardStoreProps {
  rewards: Reward[];
  userPoints: number;
  onPurchase: (rewardId: string) => void;
}

export function RewardStore({ rewards, userPoints, onPurchase }: RewardStoreProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("全部");
  
  const categories = ["全部", "玩具", "零食", "活动", "特权"];
  
  const filteredRewards = selectedCategory === "全部" 
    ? rewards 
    : rewards.filter(reward => reward.category === selectedCategory);

  const getCategoryColor = (category: string) => {
    switch (category) {
      case "玩具": return "accent";
      case "零食": return "secondary";
      case "活动": return "success";
      case "特权": return "default";
      default: return "outline";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Gift className="w-6 h-6 text-accent" />
          积分商城
        </h2>
        <div className="flex items-center gap-2 bg-gradient-primary text-white px-4 py-2 rounded-full">
          <Star className="w-4 h-4" />
          <span className="font-bold">{userPoints.toLocaleString()} 积分</span>
        </div>
      </div>

      {/* Category filters */}
      <div className="flex gap-2 flex-wrap">
        {categories.map(category => (
          <Button
            key={category}
            variant={selectedCategory === category ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </Button>
        ))}
      </div>

      {/* Rewards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredRewards.map(reward => {
          const canAfford = userPoints >= reward.cost;
          
          return (
            <Card 
              key={reward.id} 
              className={`transition-all duration-300 hover:shadow-accent hover:scale-105 ${
                !reward.available ? 'opacity-50' : ''
              } ${canAfford ? 'border-accent' : ''}`}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="text-3xl bg-gradient-to-br from-accent to-accent-glow p-2 rounded-lg">
                      {reward.icon}
                    </div>
                    <div>
                      <CardTitle className="text-base">{reward.name}</CardTitle>
                      <Badge variant={getCategoryColor(reward.category) as any} className="mt-1">
                        {reward.category}
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <div className="space-y-4">
                  <p className="text-sm text-muted-foreground">{reward.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-yellow-500" />
                      <span className="font-bold text-lg">{reward.cost}</span>
                      <span className="text-sm text-muted-foreground">积分</span>
                    </div>

                    {reward.popularity && (
                      <Badge variant="outline" className="text-xs">
                        热门 #{reward.popularity}
                      </Badge>
                    )}
                  </div>

                  <Button
                    variant={canAfford ? "accent" : "outline"}
                    className="w-full"
                    onClick={() => onPurchase(reward.id)}
                    disabled={!canAfford || !reward.available}
                  >
                    <ShoppingCart className="w-4 h-4 mr-2" />
                    {!reward.available 
                      ? "暂时缺货" 
                      : !canAfford 
                        ? "积分不足" 
                        : "立即兑换"
                    }
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}