// /frontend/src/components/CodeEditor.tsx
import React, { useEffect, useRef } from 'react';
import * as monaco from 'monaco-editor';
import './CodeEditor.css';

type Props = {
  initialCode: string;
  onChange: (value: string) => void;
};

const CodeEditor: React.FC<Props> = ({ initialCode, onChange }) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor>();

  useEffect(() => {
    const container = document.getElementById('editor-container')!;
    editorRef.current = monaco.editor.create(container, {
      value: initialCode,
      language: 'javascript',
      theme: 'vs-dark',
      automaticLayout: true, // Ensures the editor resizes with its container
    });
    editorRef.current.onDidChangeModelContent(() => {
      if (editorRef.current) {
        onChange(editorRef.current.getValue());
      }
    });

    return () => {
      editorRef.current?.dispose();
    };
  }, [initialCode, onChange]);

  return <div id="editor-container" className="code-editor"></div>;
};

export default CodeEditor;
