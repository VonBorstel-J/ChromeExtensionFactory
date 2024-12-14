// /frontend/src/components/DragDropBuilder.tsx
import React, { useEffect, useRef } from 'react';
import interact from 'interactjs';
import './DragDropBuilder.css';

const DragDropBuilder: React.FC = () => {
  const draggableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (draggableRef.current) {
      interact(draggableRef.current).draggable({
        modifiers: [
          interact.modifiers.restrictRect({
            restriction: 'parent',
            endOnly: true
          })
        ],
        listeners: {
          move(event) {
            const target = event.target as HTMLElement;
            const x = (parseFloat(target.getAttribute('data-x')!) || 0) + event.dx;
            const y = (parseFloat(target.getAttribute('data-y')!) || 0) + event.dy;
            target.style.transform = `translate(${x}px, ${y}px)`;
            target.setAttribute('data-x', x.toString());
            target.setAttribute('data-y', y.toString());
          }
        }
      });
    }
  }, []);

  return <div ref={draggableRef} className="draggable">Drag me!</div>;
};

export default DragDropBuilder;
