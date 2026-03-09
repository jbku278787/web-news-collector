import { Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { TimelinePage } from "@/pages/TimelinePage";
import { CategoryPage } from "@/pages/CategoryPage";
import { SourcesPage } from "@/pages/SourcesPage";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<TimelinePage />} />
        <Route path="/category/:category" element={<CategoryPage />} />
        <Route path="/sources" element={<SourcesPage />} />
      </Route>
    </Routes>
  );
}

export default App;
