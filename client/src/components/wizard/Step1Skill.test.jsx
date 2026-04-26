import { render, screen, fireEvent } from '@testing-library/react'
import Step1Skill from './Step1Skill'

const skills = [
  { id: 1, name: 'DSA', icon_emoji: '🧮' },
  { id: 2, name: 'Web Development', icon_emoji: '🌐' },
]

describe('Step1Skill', () => {
  it('renders a card for each skill', () => {
    render(<Step1Skill skills={skills} selected={null} onSelect={() => {}} />)
    expect(screen.getByText('DSA')).toBeInTheDocument()
    expect(screen.getByText('Web Development')).toBeInTheDocument()
  })

  it('calls onSelect with the skill object when a card is clicked', () => {
    const onSelect = vi.fn()
    render(<Step1Skill skills={skills} selected={null} onSelect={onSelect} />)
    fireEvent.click(screen.getByText('DSA'))
    expect(onSelect).toHaveBeenCalledWith(skills[0])
  })

  it('marks the selected card with data-selected=true', () => {
    const { container } = render(
      <Step1Skill skills={skills} selected={skills[0]} onSelect={() => {}} />
    )
    const selected = container.querySelector('[data-selected="true"]')
    expect(selected).toBeTruthy()
    expect(selected).toHaveTextContent('DSA')
  })

  it('shows loading message when skills array is empty', () => {
    render(<Step1Skill skills={[]} selected={null} onSelect={() => {}} />)
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })
})
