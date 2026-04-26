import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/client.js'
import ProgressBar from '../components/roadmap/ProgressBar.jsx'
import RoadmapHeader from '../components/roadmap/RoadmapHeader.jsx'
import WeekTimeline from '../components/roadmap/WeekTimeline.jsx'
import TaskDrawer from '../components/roadmap/TaskDrawer.jsx'

export default function Roadmap() {
  const { id } = useParams()
  const [roadmap, setRoadmap] = useState(null)
  const [selectedWeek, setSelectedWeek] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.get(`/roadmaps/${id}`)
      .then((res) => {
        setRoadmap(res.data)
        // default to first incomplete week
        const firstIncomplete = res.data.weeks.find((w) => w.topics.some((t) => !t.completed))
        setSelectedWeek(firstIncomplete ?? res.data.weeks[0])
      })
      .catch((err) => {
        setError(err.response?.status === 404 ? 'Roadmap not found.' : 'Failed to load roadmap.')
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleToggle = async (topicId, completed) => {
    // Optimistic update
    const updated = updateTopicInRoadmap(roadmap, topicId, completed)
    setRoadmap(updated)
    setSelectedWeek(updated.weeks.find((w) => w.week === selectedWeek.week) ?? null)

    try {
      const res = await api.patch(`/roadmaps/${id}/progress`, { topic_id: topicId, completed })
      setRoadmap((prev) => ({ ...prev, percent_complete: res.data.percent_complete }))
    } catch {
      // Roll back on failure
      setRoadmap(roadmap)
      setSelectedWeek(selectedWeek)
    }
  }

  if (loading) return <div className="spinner-wrap"><div className="spinner" /></div>
  if (error) return (
    <div className="page" style={{ textAlign: 'center', paddingTop: 80 }}>
      <p style={{ color: 'var(--text-muted)', marginBottom: 16 }}>{error}</p>
      <Link to="/generate">← Generate a new roadmap</Link>
    </div>
  )

  return (
    <div>
      <nav className="navbar">
        <span className="navbar-brand">✨ SmartLearning</span>
        <div style={{ display: 'flex', gap: 16 }}>
          <a href="/generate">New Roadmap</a>
          <a href="http://localhost:8080/dashboard/">Dashboard</a>
        </div>
      </nav>

      <div className="page-wide">
        <RoadmapHeader roadmap={roadmap} />
        <ProgressBar percent={roadmap.percent_complete} />

        <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 24, marginTop: 28 }}>
          <WeekTimeline
            weeks={roadmap.weeks}
            selectedWeek={selectedWeek}
            onSelect={setSelectedWeek}
          />
          <TaskDrawer week={selectedWeek} onToggle={handleToggle} />
        </div>
      </div>
    </div>
  )
}

function updateTopicInRoadmap(roadmap, topicId, completed) {
  return {
    ...roadmap,
    weeks: roadmap.weeks.map((week) => ({
      ...week,
      topics: week.topics.map((t) =>
        t.id === topicId ? { ...t, completed } : t
      ),
    })),
  }
}
