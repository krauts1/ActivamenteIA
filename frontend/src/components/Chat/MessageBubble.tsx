type Props = {
    role: "user" | "assistant"
    content: string
    sources?: any[]
  }
  
  export default function MessageBubble({ role, content, sources }: Props) {
    return (
      <div className={`bubble ${role}`}>
        <div className="content">{content}</div>
        {role === "assistant" && sources?.length ? (
          <details className="sources">
            <summary>Fuentes ({sources.length})</summary>
            <ul>
              {sources.map((s: any) => (
                <li key={s.rid}>
                  <strong>rid={s.rid}</strong> · score={typeof s.score === "number" ? s.score.toFixed(3) : s.score} ·{" "}
                  <em>{s.meta?.filename}</em>
                </li>
              ))}
            </ul>
          </details>
        ) : null}
      </div>
    )
  }
  