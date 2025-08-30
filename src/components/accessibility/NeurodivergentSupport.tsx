"use client"

export function NeurodivergentSupport() {
  return (
    <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg p-6 border border-green-200 dark:border-green-800">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-10 h-10 bg-green-100 dark:bg-green-800 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-200">
            Neurodivergent Support Active
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Your personalized accommodations are enabled
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-slate-800 rounded-lg p-4">
          <h4 className="font-medium text-slate-800 dark:text-slate-200 mb-2">ADHD Features</h4>
          <ul className="text-sm text-slate-600 dark:text-slate-400 space-y-1">
            <li>• Pomodoro timer active</li>
            <li>• Task breakdown enabled</li>
            <li>• Progress tracking on</li>
          </ul>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-lg p-4">
          <h4 className="font-medium text-slate-800 dark:text-slate-200 mb-2">Autism Support</h4>
          <ul className="text-sm text-slate-600 dark:text-slate-400 space-y-1">
            <li>• Predictable workflows</li>
            <li>• Detailed explanations</li>
            <li>• Consistent interface</li>
          </ul>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-lg p-4">
          <h4 className="font-medium text-slate-800 dark:text-slate-200 mb-2">Anxiety Management</h4>
          <ul className="text-sm text-slate-600 dark:text-slate-400 space-y-1">
            <li>• Stress monitoring</li>
            <li>• Gentle notifications</li>
            <li>• Confidence indicators</li>
          </ul>
        </div>
      </div>
    </div>
  )
}