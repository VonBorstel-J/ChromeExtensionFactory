// /frontend/src/components/CodeEditor.tsx
import React, { useEffect, useRef } from 'react';
import * as monaco from 'monaco-editor';
import styles from '../styles/CodeEditor.module.css';

type Props = {
  initialCode: string;
  onChange: (value: string) => void;
};

const CodeEditor: React.FC<Props> = ({ initialCode, onChange }) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor>();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      editorRef.current = monaco.editor.create(containerRef.current, {
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
    }

    return () => {
      editorRef.current?.dispose();
    };
  }, [initialCode, onChange]);

  return <div ref={containerRef} className={styles.codeEditor}></div>;
};

export default CodeEditor;
