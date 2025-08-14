import React from "react";
import "./ChatInput.css";

type Props = {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  disabled?: boolean;
  placeholder?: string;
};

export default function ChatInput({
  value,
  onChange,
  onSend,
  disabled,
  placeholder = "Escribe tu mensaje…",
}: Props) {
  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!disabled) onSend();
  };

  return (
    <form className="chat-input-container" onSubmit={onSubmit}>
      <input
        type="text"
        className="chat-input"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
      />
      <button type="submit" className="chat-send-btn" disabled={disabled} aria-label="Enviar">
        ➤
      </button>
    </form>
  );
}
