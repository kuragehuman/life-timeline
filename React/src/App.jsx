import "./App.css";

function App() {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const slots = Array.from({ length: 24 }, (_, i) => i);

  return (
    <div className="container">
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

      </div>
    </div>
  );
}

export default App;