"use client"

export function RecentActivity() {
  const activities = [
    {
      id: 1,
      type: 'scan_completed',
      title: 'Network scan completed',
      description: '192.168.1.0/24 - 15 hosts discovered, 3 open services',
      timestamp: '2 hours ago',
      status: 'completed'
    },
    {
      id: 2,
      type: 'vulnerability_found',
      title: 'High severity vulnerability detected',
      description: 'SSH weak authentication on 192.168.1.100',
      timestamp: '4 hours ago',
      status: 'warning'
    },
    {
      id: 3,
      type: 'report_generated',
      title: 'Penetration testing report generated',
      description: 'Executive summary and technical details ready for review',
      timestamp: '1 day ago',
      status: 'completed'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100 dark:bg-green-900/20'
      case 'warning': return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20'
      case 'error': return 'text-red-600 bg-red-100 dark:bg-red-900/20'
      default: return 'text-blue-600 bg-blue-100 dark:bg-blue-900/20'
    }
  }

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Recent Activity</h3>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50">
            <div className={`w-2 h-2 rounded-full mt-2 ${getStatusColor(activity.status)}`}></div>
            <div className="flex-1">
              <h4 className="font-medium text-slate-900 dark:text-slate-100">{activity.title}</h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">{activity.description}</p>
              <span className="text-xs text-slate-500 dark:text-slate-400">{activity.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
      <button className="mt-4 text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors">
        View all activity →
      </button>
    </div>
  )
}