"use client"

export function QuickActions() {
  const actions = [
    {
      name: 'Network Scan',
      description: 'Discover hosts and services on target networks',
      icon: '🔍',
      difficulty: 'Beginner',
      estimatedTime: '15-30 min'
    },
    {
      name: 'Vulnerability Assessment',
      description: 'Identify security weaknesses in target systems',
      icon: '🛡️',
      difficulty: 'Intermediate',
      estimatedTime: '45-90 min'
    },
    {
      name: 'Web App Testing',
      description: 'Test web applications for security flaws',
      icon: '🌐',
      difficulty: 'Intermediate',
      estimatedTime: '60-120 min'
    },
    {
      name: 'Social Engineering',
      description: 'Test human factors in security',
      icon: '👥',
      difficulty: 'Advanced',
      estimatedTime: '30-60 min'
    }
  ]

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Quick Actions</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {actions.map((action) => (
          <button
            key={action.name}
            className="text-left p-4 border border-slate-200 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
          >
            <div className="flex items-start space-x-3">
              <span className="text-2xl">{action.icon}</span>
              <div className="flex-1">
                <h4 className="font-medium text-slate-900 dark:text-slate-100">{action.name}</h4>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">{action.description}</p>
                <div className="flex items-center space-x-4 text-xs">
                  <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                    {action.difficulty}
                  </span>
                  <span className="text-slate-500 dark:text-slate-400">{action.estimatedTime}</span>
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}