import { useState } from "react"
import { useNavigate } from "react-router"
import { ArrowLeft, Download, Share, User, Calendar, Activity, AlertTriangle, FileText, Check, Copy, Loader2, ShieldAlert, CheckCircle2 } from "lucide-react"
import { Button, Card, CardContent } from "../components/ui"
import { useTriage } from "../context/TriageContext"
import { useAuth } from "../context/AuthContext"
import { api, SharedSummaryResponse } from "../lib/api"

export function ClinicianSummary() {
  const navigate = useNavigate()
  const { activeSession, currentResult, submittedSymptoms } = useTriage()
  const { user } = useAuth()

  const [shareData, setShareData] = useState<SharedSummaryResponse | null>(null)
  const [isSharing, setIsSharing] = useState(false)
  const [copied, setCopied] = useState(false)
  const [shareError, setShareError] = useState<string | null>(null)

  // Derive display values from active session or current triage result
  const patientName = activeSession?.profile_name || user?.full_name || "Self (Patient)"
  const patientAge = activeSession?.patient_age || 34
  const patientSex = activeSession?.patient_sex ? activeSession.patient_sex.charAt(0).toUpperCase() + activeSession.patient_sex.slice(1) : "Not specified"
  const urgency = activeSession?.urgency || currentResult?.urgency || "urgent_care"
  const symptomsList = activeSession?.reported_symptoms || submittedSymptoms.map((s) => s.name) || ["Headache", "Fever"]
  const durationDays = activeSession?.duration_days || 2
  const severity = activeSession?.severity_scale || (submittedSymptoms.length > 0 ? Math.max(...submittedSymptoms.map((s) => s.severity)) : 7)
  const careAdvice = activeSession?.care_advice || currentResult?.care_advice || "Patient reports onset of acute symptoms. Clinical evaluation recommended."
  const redFlags = activeSession?.red_flags_triggered || currentResult?.red_flags_triggered || []

  const formattedDate = activeSession?.created_at
    ? new Date(activeSession.created_at).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    : "Today, Recent"

  const handleShare = async () => {
    setIsSharing(true)
    setShareError(null)
    try {
      const sessionId = activeSession?.id || currentResult?.session_id
      if (!sessionId) {
        throw new Error("Please complete a triage check or select a past check from History first.")
      }
      const res = await api.createShare(sessionId)
      setShareData(res)
    } catch (err: any) {
      setShareError(err?.message || "Failed to generate shareable clinician summary.")
    } finally {
      setIsSharing(false)
    }
  }

  const handleCopyLink = () => {
    if (shareData?.share_url) {
      navigator.clipboard.writeText(shareData.share_url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2500)
    }
  }

  const handleExport = () => {
    window.print()
  }

  const getUrgencyDisplay = (urg: string) => {
    if (urg === "emergency") {
      return { label: "Emergency Care", color: "text-red-600", icon: ShieldAlert, border: "border-l-red-500" }
    }
    if (urg === "urgent_care") {
      return { label: "Urgent Care", color: "text-amber-600", icon: AlertTriangle, border: "border-l-amber-500" }
    }
    return { label: "Self-Care", color: "text-emerald-600", icon: CheckCircle2, border: "border-l-emerald-500" }
  }

  const urgDisplay = getUrgencyDisplay(urgency)
  const UrgIcon = urgDisplay.icon

  return (
    <div className="flex flex-col min-h-full bg-background pb-20">
      <div className="bg-white px-4 py-4 pt-12 border-b sticky top-0 z-10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate(-1)} className="p-2 -ml-2 rounded-full hover:bg-black/5" aria-label="Go back">
            <ArrowLeft className="w-5 h-5 text-foreground" />
          </button>
          <h1 className="text-xl font-display font-semibold">Summary</h1>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExport}
            className="p-2 rounded-full bg-secondary text-primary hover:bg-primary/20 transition-colors"
            title="Export Summary (Print/PDF)"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Share Success Modal / Card */}
        {shareData && (
          <div className="bg-teal-50 border border-teal-200 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-teal-900 uppercase tracking-wider">
                Secure Clinician Link Generated
              </span>
              <span className="text-xs text-teal-700">Valid for 72 hrs</span>
            </div>
            <p className="text-xs text-teal-800 break-all font-mono bg-white/80 p-2 rounded border border-teal-100">
              {shareData.share_url}
            </p>
            <div className="flex justify-end gap-2 pt-1">
              <Button size="sm" variant="outline" onClick={handleCopyLink} className="gap-1.5 text-xs h-8">
                {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? "Link Copied!" : "Copy Link"}
              </Button>
            </div>
          </div>
        )}

        {shareError && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl">
            {shareError}
          </div>
        )}
        
        {/* Patient Profile Header Card */}
        <Card className="bg-white border-none shadow-sm rounded-t-2xl rounded-b-md">
          <CardContent className="p-5">
            <div className="flex items-center gap-4 mb-4 pb-4 border-b border-border/50">
              <div className="w-12 h-12 bg-secondary rounded-full flex items-center justify-center text-primary font-display font-bold text-lg">
                {patientName.substring(0, 2).toUpperCase()}
              </div>
              <div>
                <h2 className="text-lg font-semibold text-foreground">{patientName}</h2>
                <p className="text-sm text-muted-foreground flex items-center gap-1.5 mt-0.5">
                  <User className="w-3.5 h-3.5" /> {patientAge} yrs • {patientSex}
                </p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground block mb-0.5">Date of log</span>
                <span className="font-medium text-foreground flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-primary" /> {formattedDate}
                </span>
              </div>
              <div>
                <span className="text-muted-foreground block mb-0.5">Triage Result</span>
                <span className={`font-medium flex items-center gap-1.5 ${urgDisplay.color}`}>
                  <UrgIcon className="w-3.5 h-3.5" /> {urgDisplay.label}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Reported Symptoms Card */}
        <Card className={`bg-white border-none shadow-sm rounded-md border-l-4 ${urgDisplay.border}`}>
          <CardContent className="p-5 space-y-4">
            <h3 className="font-medium text-foreground flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary" /> Reported Symptoms
            </h3>
            
            <div className="space-y-3">
              {symptomsList.map((sym, idx) => (
                <div key={idx}>
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="font-medium text-foreground block">{sym}</span>
                      <span className="text-xs text-muted-foreground">Duration: {durationDays} days</span>
                    </div>
                    <div className="bg-amber-100 text-amber-800 text-xs font-semibold px-2 py-0.5 rounded-full">
                      Severity ({severity}/10)
                    </div>
                  </div>
                  {idx < symptomsList.length - 1 && <div className="h-px w-full bg-border/50 mt-3" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Red Flags / Clinical Advice Card */}
        <Card className="bg-white border-none shadow-sm rounded-b-2xl rounded-t-md">
          <CardContent className="p-5 space-y-2">
            <h3 className="font-medium text-foreground flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-primary" /> Notes for Clinician
            </h3>

            {redFlags.length > 0 && (
              <div className="p-3 bg-red-50 border border-red-100 text-red-800 rounded-lg text-xs space-y-1">
                <span className="font-semibold block">⚠️ Red Flags Triggered:</span>
                {redFlags.map((rf, idx) => (
                  <p key={idx}>• {rf}</p>
                ))}
              </div>
            )}

            <p className="text-sm text-foreground/80 leading-relaxed bg-muted/50 p-3 rounded-lg border border-border/50">
              {careAdvice}
            </p>
          </CardContent>
        </Card>

      </div>

      <div className="p-4 mt-auto">
        <Button 
          className="w-full gap-2 h-14 text-base shadow-lg shadow-primary/20"
          onClick={handleShare}
          disabled={isSharing}
        >
          {isSharing ? <Loader2 className="w-5 h-5 animate-spin" /> : <Share className="w-5 h-5" />}
          {isSharing ? "Generating Link..." : "Share with Clinician"}
        </Button>
      </div>
    </div>
  )
}
