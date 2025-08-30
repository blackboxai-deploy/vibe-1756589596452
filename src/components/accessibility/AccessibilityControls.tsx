"use client"

import { useState } from 'react'
import { useAccessibility } from '../../providers/AccessibilityProvider'

export function AccessibilityControls() {
  const [isOpen, setIsOpen] = useState(false)
  const { settings, updateSettings } = useAccessibility()

  return (
    <div className="fixed top-4 right-4 z-40">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transition-colors"
        aria-label="Accessibility Settings"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-16 right-0 bg-white dark:bg-slate-800 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 p-6 w-80">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
            Accessibility Settings
          </h3>

          <div className="space-y-4">
            {/* Theme Selection */}
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Theme
              </label>
              <select
                value={settings.theme}
                onChange={(e) => updateSettings({ theme: e.target.value as any })}
                className="w-full p-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="high-contrast">High Contrast</option>
                <option value="calm">Calm (Recommended)</option>
              </select>
            </div>

            {/* Font Size */}
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Font Size
              </label>
              <select
                value={settings.fontSize}
                onChange={(e) => updateSettings({ fontSize: e.target.value as any })}
                className="w-full p-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
                <option value="extra-large">Extra Large</option>
              </select>
            </div>

            {/* Neurodivergent Support Options */}
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Neurodivergent Support
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.neurodivergentSupport.adhd}
                    onChange={(e) => updateSettings({
                      neurodivergentSupport: {
                        ...settings.neurodivergentSupport,
                        adhd: e.target.checked
                      }
                    })}
                    className="mr-2 rounded"
                  />
                  <span className="text-sm text-slate-700 dark:text-slate-300">ADHD Support</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.neurodivergentSupport.autism}
                    onChange={(e) => updateSettings({
                      neurodivergentSupport: {
                        ...settings.neurodivergentSupport,
                        autism: e.target.checked
                      }
                    })}
                    className="mr-2 rounded"
                  />
                  <span className="text-sm text-slate-700 dark:text-slate-300">Autism Support</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.neurodivergentSupport.anxiety}
                    onChange={(e) => updateSettings({
                      neurodivergentSupport: {
                        ...settings.neurodivergentSupport,
                        anxiety: e.target.checked
                      }
                    })}
                    className="mr-2 rounded"
                  />
                  <span className="text-sm text-slate-700 dark:text-slate-300">Anxiety Support</span>
                </label>
              </div>
            </div>

            {/* Focus Mode Toggle */}
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Focus Mode</span>
              <button
                onClick={() => updateSettings({ focusMode: !settings.focusMode })}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.focusMode ? 'bg-blue-600' : 'bg-slate-200 dark:bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.focusMode ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}