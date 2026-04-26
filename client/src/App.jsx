import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import Generator from './pages/Generator.jsx'
import Roadmap from './pages/Roadmap.jsx'

function TokenCapture() {
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const token = params.get('token')
    if (token) {
      localStorage.setItem('authToken', token)
      navigate('/generate', { replace: true })
    } else if (!localStorage.getItem('authToken')) {
      window.location.href = 'http://localhost:8080/users/login/'
    } else {
      navigate('/generate', { replace: true })
    }
  }, [])

  return null
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<TokenCapture />} />
        <Route path="/generate" element={<Generator />} />
        <Route path="/roadmap/:id" element={<Roadmap />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
