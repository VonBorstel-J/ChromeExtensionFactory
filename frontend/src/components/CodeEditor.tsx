// /frontend/src/components/CodeEditor.tsx
import React, { useEffect, useRef } from 'react';
import * as monaco from 'monaco-editor';

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

  return <div id="editor-container" style={{ height: '400px', border: '1px solid #ccc' }}></div>;
};

export default CodeEditor;
