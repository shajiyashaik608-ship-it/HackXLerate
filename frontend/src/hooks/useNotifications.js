import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for managing Web Notifications API permissions and scheduled alerts
 */
export function useNotifications() {
  const [permission, setPermission] = useState(
    typeof window !== 'undefined' && 'Notification' in window
      ? Notification.permission
      : 'unsupported'
  );
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    if (typeof window === 'undefined' || !('Notification' in window)) {
      setIsSupported(false);
      setPermission('unsupported');
    } else {
      setPermission(Notification.permission);
    }
  }, []);

  const requestPermission = useCallback(async () => {
    if (!isSupported || !('Notification' in window)) {
      return 'unsupported';
    }

    try {
      const result = await Notification.requestPermission();
      setPermission(result);
      return result;
    } catch (err) {
      console.warn('Error requesting notification permission:', err);
      return 'denied';
    }
  }, [isSupported]);

  const sendNotification = useCallback((title, options = {}) => {
    if (!isSupported || permission !== 'granted') {
      return false;
    }

    try {
      new Notification(title, {
        icon: '/favicon.svg',
        badge: '/favicon.svg',
        ...options
      });
      return true;
    } catch (e) {
      console.warn('Notification send failed:', e);
      return false;
    }
  }, [isSupported, permission]);

  return {
    permission,
    isSupported,
    requestPermission,
    sendNotification
  };
}
