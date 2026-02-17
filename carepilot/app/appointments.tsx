import React, { useEffect, useState } from "react";
import { View, Text, ScrollView, RefreshControl } from "react-native";
import api from "../api";
import { Ionicons } from "@expo/vector-icons";

export default function AppointmentsScreen() {
  const [appointments, setAppointments] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const loadAppointments = async () => {
    try {
      const res = await api.get("/appointments/");
      setAppointments(res.data.appointments || []);
    } catch (err) {
      console.log(err);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadAppointments();
    setRefreshing(false);
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  return (
    <ScrollView
      className="flex-1 bg-white p-4"
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <Text className="text-2xl font-bold mb-4 text-center">
        Booked Appointment Slots
      </Text>

      {appointments.length === 0 ? (
        <Text className="text-center text-gray-500 mt-4">
          No appointments found.
        </Text>
      ) : (
        appointments.map((item, idx) => (
          <View
            key={idx}
            className="flex-row items-center bg-blue-50 border border-blue-200 p-4 rounded-xl mb-3"
          >
            <Ionicons name="calendar-outline" size={26} color="#2563EB" />
            <View className="ml-3">
              <Text className="text-blue-700 font-semibold">{item}</Text>
            </View>
          </View>
        ))
      )}
    </ScrollView>
  );
}
