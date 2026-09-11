import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, Button } from "../components/ui"
import { Activity, Users, FileText, Server, Search, Plus, ArrowUpRight, Loader2, Check, X, AlertCircle } from "lucide-react"
import { api, ConditionItem } from "../lib/api"

export function AdminPanel() {
  const [conditions, setConditions] = useState<ConditionItem[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [systemHealth, setSystemHealth] = useState<string>("Checking...")
  const [isOperational, setIsOperational] = useState(true)
  
  // Modal state for adding a condition
  const [showAddModal, setShowAddModal] = useState(false)
  const [newCode, setNewCode] = useState("")
  const [newName, setNewName] = useState("")
  const [newCategory, setNewCategory] = useState("General")
  const [newUrgency, setNewUrgency] = useState("self_care")
  const [newDesc, setNewDesc] = useState("")
  const [newCare, setNewCare] = useState("")
  const [addError, setAddError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const loadData = () => {
    setIsLoading(true)
    Promise.all([
      api.getConditions(searchTerm).catch(() => []),
      api.getHealth().catch(() => null),
    ])
      .then(([condList, health]) => {
        setConditions(condList || [])
        if (health && health.status === "ok") {
          setSystemHealth("All systems operational")
          setIsOperational(true)
        } else {
          setSystemHealth("Degraded")
          setIsOperational(false)
        }
      })
      .finally(() => {
        setIsLoading(false)
      })
  }

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      api.getConditions(searchTerm)
        .then((list) => setConditions(list || []))
        .catch(() => {})
    }, 300)
    return () => clearTimeout(timer)
  }, [searchTerm])

  const handleAddCondition = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newCode || !newName) {
      setAddError("Code and Name are required.")
      return
    }
    setAddError(null)
    setIsSubmitting(true)
    try {
      await api.createCondition({
        code: newCode.trim().toLowerCase().replace(/\s+/g, "_"),
        name: newName.trim(),
        category: newCategory,
        typical_urgency: newUrgency,
        description: newDesc.trim() || undefined,
        care_recommendations: newCare.trim() || undefined,
      })
      setShowAddModal(false)
      setNewCode("")
      setNewName("")
      setNewDesc("")
      setNewCare("")
      loadData()
    } catch (err: any) {
      setAddError(err?.message || "Failed to create condition entry.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const getUrgencyBadge = (urg: string) => {
    if (urg === "emergency") return { label: "Emergency", color: "bg-red-100 text-red-700" }
    if (urg === "urgent_care") return { label: "Urgent Care", color: "bg-amber-100 text-amber-700" }
    return { label: "Self-Care", color: "bg-green-100 text-green-700" }
  }

  return (
    <div className="p-6 md:p-8 space-y-8 max-w-6xl mx-auto">
      
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-semibold">Clinical Operations Dashboard</h1>
          <p className="text-muted-foreground text-sm mt-1">Overview of clinical knowledge base and platform health.</p>
        </div>
        <div className="flex items-center gap-3 bg-white px-4 py-2 rounded-xl border shadow-sm">
          <div className={`w-2.5 h-2.5 rounded-full ${isOperational ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
          <span className="text-sm font-medium">{systemHealth}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {[
          { label: "Active Users", value: "1,240", change: "+12%", icon: Users, color: "text-blue-600", bg: "bg-blue-100" },
          { label: "Knowledge Conditions", value: conditions.length.toString(), change: "+Active", icon: Activity, color: "text-teal-600", bg: "bg-teal-100" },
          { label: "Completion Rate", value: "96.4%", change: "+2.1%", icon: FileText, color: "text-indigo-600", bg: "bg-indigo-100" },
          { label: "API Uptime", value: isOperational ? "100.0%" : "99.8%", change: "0.0%", icon: Server, color: "text-emerald-600", bg: "bg-emerald-100" },
        ].map((stat, i) => (
          <Card key={i} className="border-none shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-5 h-5" />
                </div>
                <div className="flex items-center gap-1 text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded-full">
                  <ArrowUpRight className="w-3 h-3" /> {stat.change}
                </div>
              </div>
              <div>
                <h3 className="text-3xl font-display font-bold tracking-tight text-foreground">{stat.value}</h3>
                <p className="text-sm font-medium text-muted-foreground mt-1">{stat.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="border-none shadow-sm">
        <CardHeader className="flex flex-row items-center justify-between border-b pb-4">
          <CardTitle className="text-lg">Knowledge Base Management</CardTitle>
          <button 
            onClick={() => setShowAddModal(true)}
            className="bg-primary text-primary-foreground hover:bg-primary/90 px-3 py-1.5 rounded-lg text-sm font-medium inline-flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <Plus className="w-4 h-4" /> Add Entry
          </button>
        </CardHeader>
        <CardContent className="p-0">
          <div className="p-4 border-b bg-muted/20">
            <div className="relative max-w-sm">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Search conditions or categories..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-white border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              />
            </div>
          </div>
          
          <div className="overflow-x-auto">
            {isLoading ? (
              <div className="flex items-center justify-center p-8 gap-2 text-muted-foreground text-sm">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Loading conditions...</span>
              </div>
            ) : (
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-muted-foreground uppercase bg-muted/30 border-b">
                  <tr>
                    <th className="px-6 py-3 font-medium">Condition Name</th>
                    <th className="px-6 py-3 font-medium">Category</th>
                    <th className="px-6 py-3 font-medium">Base Urgency</th>
                    <th className="px-6 py-3 font-medium">Description</th>
                  </tr>
                </thead>
                <tbody className="divide-y text-foreground/80">
                  {conditions.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-8 text-center text-muted-foreground">
                        No conditions found matching "{searchTerm}".
                      </td>
                    </tr>
                  ) : (
                    conditions.map((row) => {
                      const urg = getUrgencyBadge(row.typical_urgency)
                      return (
                        <tr key={row.id} className="hover:bg-muted/10 transition-colors">
                          <td className="px-6 py-4 font-medium text-foreground">
                            <div>{row.name}</div>
                            <span className="text-[11px] text-muted-foreground font-mono">{row.code}</span>
                          </td>
                          <td className="px-6 py-4 font-medium text-xs text-muted-foreground">{row.category}</td>
                          <td className="px-6 py-4">
                            <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${urg.color}`}>
                              {urg.label}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-xs text-muted-foreground max-w-sm truncate">
                            {row.description || "Clinical diagnosis entity in rule engine."}
                          </td>
                        </tr>
                      )
                    })
                  )}
                </tbody>
              </table>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Add Condition Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-semibold text-lg">Add Clinical Condition</h3>
              <button onClick={() => setShowAddModal(false)} className="text-muted-foreground hover:text-foreground">
                <X className="w-5 h-5" />
              </button>
            </div>

            {addError && (
              <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{addError}</span>
              </div>
            )}

            <form onSubmit={handleAddCondition} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Code (Unique identifier)</label>
                <input 
                  type="text" 
                  placeholder="e.g. acute_bronchitis" 
                  value={newCode} 
                  onChange={(e) => setNewCode(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Condition Name</label>
                <input 
                  type="text" 
                  placeholder="e.g. Acute Bronchitis" 
                  value={newName} 
                  onChange={(e) => setNewName(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Category</label>
                  <input 
                    type="text" 
                    placeholder="e.g. Respiratory" 
                    value={newCategory} 
                    onChange={(e) => setNewCategory(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Typical Urgency</label>
                  <select 
                    value={newUrgency} 
                    onChange={(e) => setNewUrgency(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary bg-white"
                  >
                    <option value="self_care">Self-Care</option>
                    <option value="urgent_care">Urgent Care</option>
                    <option value="emergency">Emergency</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Description</label>
                <textarea 
                  rows={2}
                  placeholder="Description of condition..."
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Care Recommendations</label>
                <textarea 
                  rows={2}
                  placeholder="Recommendations for patient..."
                  value={newCare}
                  onChange={(e) => setNewCare(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : "Save Entry"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  )
}
