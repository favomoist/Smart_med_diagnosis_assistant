import { useNavigate } from "react-router"
import { AlertTriangle, Phone, ArrowRight, ShieldCheck, Clock, ArrowLeft, ShieldAlert, CheckCircle } from "lucide-react"
import { Button, Card, CardContent } from "../components/ui"
import { useTriage } from "../context/TriageContext"

export function TriageResult() {
  const navigate = useNavigate()
  const { currentResult } = useTriage()

  // Fallback defaults if user navigated directly without a triage check
  const urgency = currentResult?.urgency || "urgent_care"
  const careAdvice = currentResult?.care_advice || "Based on your symptoms, we recommend consulting a healthcare professional within the next 24 hours."
  const redFlags = currentResult?.red_flags_triggered || []
  const conditionsCount = currentResult?.possible_conditions?.length || 0

  const isEmergency = urgency === "emergency"
  const isUrgent = urgency === "urgent_care"
  const isSelfCare = urgency === "self_care"

  return (
    <div className="flex flex-col min-h-full bg-background pb-20">
      <div className="px-4 py-4 pt-12 sticky top-0 z-10 flex items-center">
        <button onClick={() => navigate(-1)} className="p-2 -ml-2 rounded-full hover:bg-black/5" aria-label="Go back">
          <ArrowLeft className="w-5 h-5 text-foreground" />
        </button>
      </div>

      <div className="px-6 space-y-6 flex-1 flex flex-col items-center">
        
        {/* Urgency Icon Circle */}
        <div className={`w-24 h-24 rounded-full flex items-center justify-center shadow-inner mt-4 mb-2 ${
          isEmergency 
            ? "bg-red-100 text-red-600 animate-pulse" 
            : isUrgent 
            ? "bg-amber-100 text-amber-600" 
            : "bg-emerald-100 text-emerald-600"
        }`}>
          {isEmergency ? (
            <ShieldAlert className="w-10 h-10" />
          ) : isUrgent ? (
            <AlertTriangle className="w-10 h-10" />
          ) : (
            <CheckCircle className="w-10 h-10" />
          )}
        </div>
        
        {/* Urgency Header */}
        <div className="text-center space-y-2">
          <div className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wider mb-2 ${
            isEmergency 
              ? "border-red-200 bg-red-50 text-red-800" 
              : isUrgent 
              ? "border-amber-200 bg-amber-50 text-amber-800" 
              : "border-emerald-200 bg-emerald-50 text-emerald-800"
          }`}>
            {isEmergency ? "Emergency Alert" : isUrgent ? "Urgent Care Needed" : "Self-Care Recommended"}
          </div>

          <h1 className="text-2xl font-display font-semibold">
            {isEmergency ? "Immediate Care Required" : isUrgent ? "Seek Care Soon" : "Monitor & Rest"}
          </h1>

          <p className="text-muted-foreground text-sm max-w-[280px] mx-auto leading-relaxed">
            {isEmergency 
              ? "Your symptoms suggest a critical situation requiring emergency attention." 
              : isUrgent 
              ? "We recommend consulting a healthcare provider within 24 to 48 hours." 
              : "Your symptoms appear manageable with supportive self-care at home."}
          </p>
        </div>

        {/* Red Flag Warnings Banner (if any) */}
        {redFlags.length > 0 && (
          <div className="w-full bg-red-50 border border-red-200 rounded-xl p-4 text-left space-y-1.5">
            <div className="flex items-center gap-2 text-red-800 font-semibold text-sm">
              <ShieldAlert className="w-4 h-4 text-red-600" />
              <span>Red Flag Warnings Detected</span>
            </div>
            {redFlags.map((flag, idx) => (
              <p key={idx} className="text-xs text-red-700 leading-snug">
                • {flag}
              </p>
            ))}
          </div>
        )}

        {/* Clinical Advice Card */}
        <Card className="w-full bg-white border-none shadow-md">
          <CardContent className="p-0">
            <div className="p-4 border-b flex items-start gap-3">
              <div className="p-2 bg-secondary text-primary rounded-lg mt-0.5">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium text-foreground">Clinical Guidance</h3>
                <p className="text-sm text-muted-foreground mt-1 leading-snug">
                  {careAdvice}
                </p>
              </div>
            </div>
            
            <button 
              onClick={() => navigate("/patient/conditions")}
              className="w-full p-4 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-secondary text-primary rounded-lg">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Possible Causes ({conditionsCount})</h3>
                  <p className="text-xs text-muted-foreground mt-0.5">View matched clinical context & confidence</p>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
            </button>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="w-full space-y-3 pt-6 mt-auto">
          {isEmergency ? (
            <Button 
              className="w-full gap-2 text-lg h-14 bg-red-600 hover:bg-red-700 text-white border-transparent"
              onClick={() => window.open("tel:911")}
            >
              <Phone className="w-5 h-5" /> Call Emergency (911)
            </Button>
          ) : isUrgent ? (
            <Button className="w-full gap-2 text-lg h-14 bg-amber-500 hover:bg-amber-600 text-white border-transparent">
              <Phone className="w-5 h-5" /> Find Urgent Care
            </Button>
          ) : (
            <Button 
              className="w-full gap-2 text-lg h-14 bg-teal-600 hover:bg-teal-700 text-white border-transparent"
              onClick={() => navigate("/patient/conditions")}
            >
              <ShieldCheck className="w-5 h-5" /> Review Care Advice
            </Button>
          )}

          <Button 
            variant="outline" 
            className="w-full h-14 bg-white" 
            onClick={() => navigate("/patient/summary")}
          >
            Save for Clinician
          </Button>
        </div>
      </div>
    </div>
  )
}
