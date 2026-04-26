import { render, screen, fireEvent } from '@testing-library/react'
import TaskDrawer from './TaskDrawer'

const week = {
  week: 1,
  title: 'Arrays',
  topics: [
    {
      id: 7,
      title: 'Array fundamentals',
      estimated_hours: 2,
      completed: false,
      resources: [
        { id: 1, title: 'Arrays Crash Course', url: 'https://example.com', resource_type: 'video' },
      ],
    },
  ],
}

describe('TaskDrawer', () => {
  it('renders the week title', () => {
    render(<TaskDrawer week={week} onToggle={() => {}} />)
    expect(screen.getByText('Week 1: Arrays')).toBeInTheDocument()
  })

  it('renders a checkbox for each topic', () => {
    render(<TaskDrawer week={week} onToggle={() => {}} />)
    expect(screen.getAllByRole('checkbox')).toHaveLength(1)
  })

  it('calls onToggle(topicId, true) when unchecked box is clicked', () => {
    const onToggle = vi.fn()
    render(<TaskDrawer week={week} onToggle={onToggle} />)
    fireEvent.click(screen.getByRole('checkbox'))
    expect(onToggle).toHaveBeenCalledWith(7, true)
  })

  it('calls onToggle(topicId, false) when checked box is clicked', () => {
    const completedWeek = {
      ...week,
      topics: [{ ...week.topics[0], completed: true }],
    }
    const onToggle = vi.fn()
    render(<TaskDrawer week={completedWeek} onToggle={onToggle} />)
    fireEvent.click(screen.getByRole('checkbox'))
    expect(onToggle).toHaveBeenCalledWith(7, false)
  })

  it('renders resource links that open in new tab', () => {
    render(<TaskDrawer week={week} onToggle={() => {}} />)
    const link = screen.getByText('Arrays Crash Course')
    expect(link.tagName).toBe('A')
    expect(link).toHaveAttribute('href', 'https://example.com')
    expect(link).toHaveAttribute('target', '_blank')
  })
})
