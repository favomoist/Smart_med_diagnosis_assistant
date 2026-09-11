import { useState } from "react"
import { useNavigate } from "react-router"
import { ArrowLeft, ChevronDown, ChevronUp, Info, HelpCircle } from "lucide-react"
import { Card, CardContent, Badge } from "../components/ui"
import { useTriage } from "../context/TriageContext"
import { MatchedCondition } from "../lib/api"

export function PossibleConditions() {
  const navigate = useNavigate()
  const { currentResult } = useTriage()

  const conditions: MatchedCondition[] = currentResult?.possible_conditions || []
  const [expandedCode, setExpandedCode] = useState<string | null>(() => {
    return conditions.length > 0 ? conditions[0].condition_code : null
  })

  return (
    <div className="flex flex-col min-h-full bg-background pb-24">
      <div className="bg-white px-4 py-4 pt-12 border-b sticky top-0 z-10 flex items-center gap-3">
        <button onClick={() => navigate(-1)} className="p-2 -ml-2 rounded-full hover:bg-black/5" aria-label="Go back">
          <ArrowLeft className="w-5 h-5 text-foreground" />
        </button>
        <h1 className="text-xl font-display font-semibold">Possible Causes</h1>
      </div>

      <div className="p-4">
        {/* Disclaimer Banner */}
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 flex gap-3 mb-6">
          <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <p className="text-sm text-blue-900 leading-snug">
            <strong>Not a diagnosis.</strong> This list is informational based on clinical matching against your reported symptoms and does not substitute for a professional medical consultation.
          </p>
        </div>

        {conditions.length === 0 ? (
          <div className="text-center py-12 px-4 space-y-3">
            <div className="w-12 h-12 bg-secondary rounded-full flex items-center justify-center mx-auto text-muted-foreground">
              <HelpCircle className="w-6 h-6" />
            </div>
            <h3 className="font-semibold text-foreground">No specific condition matches found</h3>
            <p className="text-sm text-muted-foreground max-w-xs mx-auto">
              Your reported symptoms did not strongly correlate with specific mapped conditions in our catalog. A primary care evaluation is recommended.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {conditions.map((condition) => {
              const isExpanded = expandedCode === condition.condition_code
              const matchPercent = Math.round(condition.confidence_score)
              const badgeVariant =
                condition.confidence_level === "High"
                  ? "default"
                  : condition.confidence_level === "Medium"
                  ? "secondary"
                  : "outline"

              return (
                <Card 
                  key={condition.condition_code} 
                  className={`overflow-hidden transition-all duration-200 border-transparent shadow-sm ${
                    isExpanded ? 'ring-2 ring-primary/20 bg-white' : 'bg-white/60 hover:bg-white'
                  }`}
                >
                  <div 
                    className="p-4 flex items-start justify-between cursor-pointer"
                    onClick={() => setExpandedCode(isExpanded ? null : condition.condition_code)}
                  >
                    <div className="space-y-2 flex-1">
                      <div className="flex justify-between items-start mr-4">
                        <div>
                          <h3 className="font-semibold text-foreground">{condition.condition_name}</h3>
                          <span className="text-xs text-muted-foreground">{condition.category}</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Badge variant={badgeVariant}>
                          {condition.confidence_level} Likelihood
                        </Badge>
                        <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-primary rounded-full opacity-80"
                            style={{ width: `${matchPercent}%` }}
                          />
                        </div>
                        <span className="text-xs text-muted-foreground font-mono">{matchPercent}%</span>
                      </div>
                    </div>

                    <div className="p-1 text-muted-foreground mt-1">
                      {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </div>
                  </div>
                  
                  {isExpanded && (
                    <CardContent className="px-4 pb-4 pt-0 space-y-3">
                      <div className="pt-3 border-t border-border/50">
                        <h4 className="text-xs font-semibold text-foreground uppercase tracking-wider mb-1">Description</h4>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {condition.description || "Common medical condition associated with these symptoms."}
                        </p>
                      </div>

                      {condition.care_recommendations && (
                        <div className="pt-2 border-t border-border/50">
                          <h4 className="text-xs font-semibold text-foreground uppercase tracking-wider mb-1">Care Recommendations</h4>
                          <p className="text-sm text-foreground/85 leading-relaxed bg-teal-50/60 p-2.5 rounded-lg border border-teal-100">
                            {condition.care_recommendations}
                          </p>
                        </div>
                      )}
                    </CardContent>
                  )}
                </Card>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
