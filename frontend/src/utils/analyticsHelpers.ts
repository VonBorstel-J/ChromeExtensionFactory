// /frontend/src/utils/analyticsHelpers.ts

interface EventData {
  [key: string]: any;
}

export const trackEvent = (event: string, data: EventData = {}) => {
  // Implement analytics tracking logic, e.g., send to Google Analytics or another service
  console.log(`Tracking event: ${event}`, data);
  // Example:
  // window.ga('send', 'event', event, data);
};
