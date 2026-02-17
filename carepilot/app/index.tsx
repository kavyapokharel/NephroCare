import React, { useEffect, useState } from 'react';
import { Alert, View, Text, TouchableOpacity, FlatList, StatusBar, ActivityIndicator, ScrollView, Modal } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, Link } from 'expo-router';
import api from '../api';
import '../global.css';
import { Picker } from '@react-native-picker/picker';

export default function App() {
  const navigation = useNavigation();

  const [loading, setLoading] = useState(true);
  const [goalList, setGoalList] = useState([]);
  const [selectedGoal, setSelectedGoal] = useState('');
  const [goalLog, setGoalLog] = useState(null);
  const [loadingGoal, setLoadingGoal] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const [summaryVisible, setSummaryVisible] = useState(false);
  const [healthSummary, setHealthSummary] = useState('');

  function formatSummary(text) {
    return text.split('\n\n').map((para, i) => (
      <Text key={i} className="text-gray-800 mb-3 leading-6">
        {para.trim().replace(/^“|”$/g, '')}
      </Text>
    ));
  }

  async function getHealthSummary() {
    try {
      const response = await api.post('health-summary/', {}, { timeout: 300000 });
      setHealthSummary(response.data);
      setSummaryVisible(true);
    } catch (e) {
      Alert.alert("Error", e.message);
    }
  }

  async function loadGoalList() {
    try {
      const res = await api.get('goal/');
      setGoalList(res.data || []);
    } catch (e) {
      Alert.alert("Failed to get data!", e?.message || e);
    }
  }

  async function fetchGoalLog(goal) {
    setLoadingGoal(true);
    try {
      const res = await api.post('goal/', { goal });
      setGoalLog(res.data);
    } catch (e) {
      Alert.alert("Failed to load goal log", e?.message || e);
    } finally {
      setLoadingGoal(false);
    }
  }

  useEffect(() => {
    loadGoalList();
    setLoading(false);
  }, []);

  useEffect(() => {
    if (selectedGoal !== '') fetchGoalLog(selectedGoal);
    else setGoalLog(null);
  }, [selectedGoal]);

  const gridButtons = [
    { key: 'appointments', title: 'Appointments & Reminders', navigate: 'appointments', icon: <Ionicons name="calendar-outline" size={26} /> },
    { key: 'yourHealth', title: 'Health Tips', navigate: 'tips', icon: <MaterialCommunityIcons name="robot" size={26} /> },
    { key: 'logs', title: 'Health Graph', navigate: 'health_graph', icon: <Ionicons name="list-outline" size={26} /> },
    { key: 'expenditure', title: 'Healthcare Expenditure', navigate: 'expenditure', icon: <Ionicons name="card-outline" size={26} /> }
  ];

  return (
    <SafeAreaView className="flex-1 bg-white">
      <StatusBar barStyle="dark-content" />

      <View className="px-4 py-3 flex-row items-center justify-between">
        <TouchableOpacity onPress={() => setDrawerOpen(true)}>
          <Ionicons name="menu" size={28} />
        </TouchableOpacity>

        <View className="flex-col items-center">
          <Text className="text-lg font-semibold">Hello, Sugam</Text>
          <Text className="text-xs text-gray-500 mt-[-2]">Hattiesburg Health & Dialysis Clinic</Text>
        </View>

        <TouchableOpacity onPress={() => setDrawerOpen(true)}>
          <Ionicons name="notifications-outline" size={26} />
        </TouchableOpacity>
      </View>

      {drawerOpen && (
        <View className="absolute top-0 left-0 h-full w-full bg-black/40 z-50">
          <TouchableOpacity className="flex-1" onPress={() => setDrawerOpen(false)} activeOpacity={1} />
          <View className="absolute top-0 left-0 h-full w-72 bg-white shadow-xl p-5">
            <Text className="text-xl font-bold mb-5">Menu</Text>

            <TouchableOpacity className="py-3 border-b" onPress={() => alert("Insurance & Policy clicked")}>
              <Text className="text-base">Insurance & Policy</Text>
            </TouchableOpacity>

            <TouchableOpacity className="py-3 border-b" onPress={() => alert("Your Health Provider clicked")}>
              <Text className="text-base">Your Health Provider</Text>
            </TouchableOpacity>

            <Text className="text-lg font-semibold mt-6 mb-3">Notifications</Text>

            <View className="bg-gray-100 rounded-lg p-3 mb-2">
              <Text className="font-medium">Your appointment is tomorrow at 9:00 AM</Text>
              <Text className="text-xs text-gray-500">1 day ago</Text>
            </View>

            <View className="bg-gray-100 rounded-lg p-3 mb-2">
              <Text className="font-medium">New health tip available</Text>
              <Text className="text-xs text-gray-500">3 days ago</Text>
            </View>

            <View className="bg-gray-100 rounded-lg p-3">
              <Text className="font-medium">Insurance policy updated</Text>
              <Text className="text-xs text-gray-500">1 week ago</Text>
            </View>
          </View>
        </View>
      )}

      <ScrollView showsVerticalScrollIndicator={false}>
        <View className="m-5 p-5 rounded-2xl bg-blue-50 shadow-sm">
          <Text className="font-bold text-lg mb-3">Your Health Goal</Text>

          <View className="border rounded-xl bg-white shadow-sm">
            <Picker selectedValue={selectedGoal} onValueChange={(val) => setSelectedGoal(val)}>
              <Picker.Item label="Select your goal..." value="" />
              {goalList.map((g) => (
                <Picker.Item key={g} label={g} value={g} />
              ))}
            </Picker>
          </View>

          <View className="mt-4">
            {loadingGoal ? (
              <ActivityIndicator size="small" color="blue" />
            ) : selectedGoal === '' ? (
              <Text className="text-gray-600 mt-2">Choose a goal to view progress.</Text>
            ) : (
              <View className="bg-white p-4 rounded-xl shadow-sm mt-2">
                <Text className="font-semibold text-base mb-2">Progress Log</Text>

                <ScrollView style={{ maxHeight: 120 }}>
                  <Text className="text-gray-800 leading-5 whitespace-pre-wrap">{goalLog}</Text>
                </ScrollView>
              </View>
            )}
          </View>
        </View>

        <View className="mx-4 p-4 rounded-xl border border-amber-400 bg-amber-50 items-center">
          <Link className="font-bold text-base" href="/need_consultation">
            Need Consultation?
          </Link>
        </View>

        <View className="px-3 mt-3">
          <FlatList
            numColumns={2}
            data={gridButtons}
            scrollEnabled={false}
            keyExtractor={(item) => item.key}
            columnWrapperStyle={{ justifyContent: 'space-between' }}
            renderItem={({ item }) => (
              <TouchableOpacity className="w-[48%] h-32 bg-gray-100 rounded-2xl items-center justify-center shadow-sm mb-3">
                {item.icon}
                <Link href={item.navigate} className="mt-2 text-center font-semibold">
                  {item.title}
                </Link>
              </TouchableOpacity>
            )}
          />
        </View>
      </ScrollView>

      <TouchableOpacity className="bg-blue-100 p-4 mx-4 mt-3 rounded-xl items-center mb-5" onPress={getHealthSummary}>
        <Text className="font-semibold text-base">My Health Summary</Text>
      </TouchableOpacity>

      <Modal visible={summaryVisible} transparent animationType="fade">
        <View className="flex-1 bg-black/40 items-center justify-center p-4">
          <View className="bg-white rounded-xl p-5 w-full max-h-[80%]">
            <Text className="text-xl font-semibold mb-4">Your Health Summary</Text>

            <ScrollView className="mb-4">
              {formatSummary(healthSummary)}
            </ScrollView>

            <TouchableOpacity className="bg-blue-500 py-2 rounded-lg" onPress={() => setSummaryVisible(false)}>
              <Text className="text-white text-center font-semibold">Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}
