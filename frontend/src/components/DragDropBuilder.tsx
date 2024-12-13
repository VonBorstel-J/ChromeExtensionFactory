import React, { useEffect, useRef } from 'react';
import interact from 'interactjs';

const DragDropBuilder = () => {
  const draggableRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (draggableRef.current) {
      interact(draggableRef.current).draggable({
        listeners: {
          move (event) {
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

  return <div ref={draggableRef} style={{width:'100px', height:'100px', background:'#ccc'}}>Drag me!</div>;
};

export default DragDropBuilder;
