import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/use-color-scheme';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Home', headerShown: false }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="modal" options={{ presentation: 'modal', title: 'Modal' }} />
        <Stack.Screen name='need_consultation' options={{title: 'Need Consultation'}} />
        <Stack.Screen name='health_graph' options={{title: 'Health Graph'}} />
        <Stack.Screen name='expenditure' options={{title: 'Expenditures'}} />
        <Stack.Screen name='tips' options={{title: 'Health Tips'}} />
        <Stack.Screen name='appointments' options={{title: 'Your Booked Appointments'}} />
      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}
