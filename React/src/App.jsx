import { useState } from "react";
import "./App.css";

function App() {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const [cardPos, setCardPos] = useState({ x: 100, y: 80 });
  const [dragging, setDragging] = useState(false);
  const slots = Array.from({ length: 24 }, (_, i) => i);

  const handleMouseDown = () => {
    setDragging(true);
  };

  const handleMouseUp = () => {
    setDragging(false);
  };

  const handleMouseMove = (e) => {
    if (!dragging) return;

    const offsetX = 80; // 曜日列
    const offsetY = 36; // ヘッダー行

    const x = e.clientX - offsetX;
    const y = e.clientY - offsetY;

    const snappedX = Math.floor(x / 64) * 64 + offsetX;
    const snappedY = Math.floor(y / 36) * 36 + offsetY;

    setCardPos({ x: snappedX, y: snappedY });
  };

  return (
    <div
      className="container"
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      <h1 className="title">生活管理シート</h1>

      <div className="grid">
        
        {/* ===== 時間ヘッダー行 ===== */}
        <div className="row">
          <div className="day"></div>

          {slots.map((i) => (
            <div key={`h-${i}`} className="cell header-cell">
              {i}
            </div>
          ))}
        </div>

        {/* ===== 曜日行 ===== */}
        {days.map((day) => (
          <div key={day} className="row">
            <div className="day">{day}</div>

            {slots.map((i) => (
              <div key={`${day}-${i}`} className="cell"></div>
            ))}
          </div>
        ))}

              {/* 仮カード */}
      <div
        className="card"
        style={{
          left: cardPos.x,
          top: cardPos.y,
        }}
        onMouseDown={handleMouseDown}
      ></div>

      </div>
    </div>
  );
}

export default App;