"use client"

export function DashboardStats() {
  const stats = [
    { name: 'Active Projects', value: '3', change: '+2', changeType: 'positive' },
    { name: 'Completed Scans', value: '127', change: '+12', changeType: 'positive' },
    { name: 'Vulnerabilities Found', value: '45', change: '-8', changeType: 'negative' },
    { name: 'Success Rate', value: '94%', change: '+2%', changeType: 'positive' }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">{stat.name}</p>
              <p className="text-2xl font-semibold text-slate-900 dark:text-slate-100">{stat.value}</p>
            </div>
            <div className={`text-sm ${stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
              {stat.change}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}