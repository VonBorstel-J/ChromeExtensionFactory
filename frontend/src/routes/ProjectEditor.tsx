// /frontend/src/routes/ProjectEditor.tsx
import React from 'react';
import styles from '../styles/ProjectEditor.module.css';
import CodeEditor from '../components/CodeEditor';
import LivePreview from '../components/LivePreview';

const ProjectEditor: React.FC = () => {
  const [code, setCode] = React.useState('// Start coding your extension here');

  return (
    <div className={styles.projectEditorContainer}>
      <h1>Project Editor</h1>
      <p>Edit your extension code, review changes, and preview updates live.</p>
      <div className={styles.editorSection}>
        <CodeEditor initialCode={code} onChange={setCode} />
        <LivePreview code={code} />
      </div>
    </div>
  );
};

export default ProjectEditor;
