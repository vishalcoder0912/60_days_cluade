import { Routes, Route } from "react-router-dom";
import Index from "./routes/index";

export default function App() {
  return (
    <Routes>
      <Route path="*" element={<Index />} />
    </Routes>
  );
}
