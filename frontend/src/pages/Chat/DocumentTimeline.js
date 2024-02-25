import React from 'react';
import { Card, Timeline } from 'antd';

export const DocumentTimeline = () => {
  return (
    <Card
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'row'
      }}
    >
      <Timeline
        items={[
          {
            children: 'Upload a PDF document'
          },
          {
            children: 'Click the bulb to get suggestions'
          },
          {
            children: 'Start chatting'
          }
        ]}
      />
    </Card>
  );
};
