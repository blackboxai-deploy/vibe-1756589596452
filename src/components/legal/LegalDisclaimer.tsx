"use client"

import { useState } from 'react'

interface LegalDisclaimerProps {
  onAccept: () => void
  onReject: () => void
}

export function LegalDisclaimer({ onAccept, onReject }: LegalDisclaimerProps) {
  const [hasRead, setHasRead] = useState(false)
  const [acknowledged, setAcknowledged] = useState(false)

  const handleAccept = () => {
    if (hasRead && acknowledged) {
      onAccept()
    }
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="bg-red-600 text-white p-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.314 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold">⚠️ CRITICAL LEGAL NOTICE</h2>
              <p className="text-red-100">FOR AUTHORIZED PENETRATION TESTING ONLY</p>
            </div>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-96">
          <div className="prose dark:prose-invert max-w-none">
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 mb-6">
              <p className="text-sm text-yellow-700 dark:text-yellow-300 font-semibold">
                UNAUTHORIZED USE OF THIS SOFTWARE IS STRICTLY PROHIBITED AND MAY RESULT IN CRIMINAL PROSECUTION
              </p>
            </div>

            <h3 className="text-xl font-bold text-slate-800 dark:text-slate-200 mb-4">
              Terms of Use and Legal Agreement
            </h3>

            <div className="space-y-4 text-slate-700 dark:text-slate-300">
              <p>
                <strong>NeuroDemon</strong> is designed exclusively for authorized security testing. 
                Users must obtain explicit written authorization before testing any systems.
              </p>

              <h4 className="font-semibold text-slate-800 dark:text-slate-200">Required Conditions:</h4>
              <ul className="list-disc pl-6 space-y-2">
                <li>Written authorization from system owners</li>
                <li>Compliance with all applicable laws</li>
                <li>Scope limitations must be respected</li>
                <li>Confidentiality of discoveries</li>
                <li>Responsible disclosure practices</li>
              </ul>

              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <h4 className="font-semibold text-red-800 dark:text-red-200 mb-2">Prohibited Activities:</h4>
                <ul className="text-red-700 dark:text-red-300 text-sm space-y-1">
                  <li>• Testing systems without explicit authorization</li>
                  <li>• Accessing data beyond authorized scope</li>
                  <li>• Causing damage or service disruption</li>
                  <li>• Violating privacy or data protection laws</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-slate-50 dark:bg-slate-700 p-6 space-y-4">
          <div className="space-y-3">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={hasRead}
                onChange={(e) => setHasRead(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
              />
              <span className="text-sm text-slate-700 dark:text-slate-300">
                I have read and understand the terms and conditions above
              </span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={acknowledged}
                onChange={(e) => setAcknowledged(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
              />
              <span className="text-sm text-slate-700 dark:text-slate-300">
                I acknowledge that I will use this software only for authorized penetration testing activities
              </span>
            </label>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <button
              onClick={onReject}
              className="flex-1 bg-slate-200 dark:bg-slate-600 text-slate-800 dark:text-slate-200 px-6 py-3 rounded-lg font-medium hover:bg-slate-300 dark:hover:bg-slate-500 transition-colors"
            >
              I Do Not Agree - Exit Application
            </button>
            <button
              onClick={handleAccept}
              disabled={!hasRead || !acknowledged}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-colors ${
                hasRead && acknowledged
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-slate-300 dark:bg-slate-600 text-slate-500 dark:text-slate-400 cursor-not-allowed'
              }`}
            >
              I Agree - Enter Application
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}