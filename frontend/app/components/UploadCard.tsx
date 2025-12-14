'use client'

import { motion } from 'framer-motion'
import { Upload } from 'lucide-react'

export default function UploadCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-3xl p-8 max-w-md w-full shadow-xl"
    >
      <h1 className="text-2xl font-semibold mb-2">
        🌸 Social Pulse
      </h1>

      <p className="text-sm text-[#6B6B6B] mb-6">
        Upload your content. Reflect. Grow gently.
      </p>

      <button className="w-full rounded-2xl bg-[#7C7CF4] text-white py-3 flex items-center justify-center gap-2 hover:opacity-90 transition">
        <Upload size={18} />
        Upload video
      </button>
    </motion.div>
  )
}