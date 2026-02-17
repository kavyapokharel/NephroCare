import React, { useEffect, useState } from "react";
import { View, Text, ScrollView, Image, RefreshControl } from "react-native";
import api from "../api";

export default function ExpenditureScreen() {
  const [imageUri, setImageUri] = useState(null);
  const [logs, setLogs] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  const loadImage = () => {
    const base = api.defaults.baseURL;
    const uri = `${base}expenditure/?t=${Date.now()}`;
    setImageUri(uri);
  };

  const loadLogs = async () => {
    try {
      const res = await api.get("/expenditure/?logs=1");
      setLogs(res.data.logs);
    } catch (err) {
      console.log(err);
    }
  };

  const reloadAll = async () => {
    setRefreshing(true);
    loadImage();
    await loadLogs();
    setRefreshing(false);
  };

  useEffect(() => {
    reloadAll();
  }, []);

  return (
    <ScrollView
      className="flex-1 bg-white p-4"
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={reloadAll} />
      }
    >
      <Text className="text-2xl font-bold mb-4 text-center">
        Expenditure Overview
      </Text>

      {imageUri && (
        <Image
          source={{ uri: imageUri }}
          className="w-full h-80 rounded-xl border mb-6"
          resizeMode="contain"
        />
      )}

      {/* Logs */}
      <View className="p-4 bg-gray-100 rounded-xl">
        <Text className="text-xl font-semibold mb-2">Expense Logs</Text>
        <Text className="font-mono text-sm whitespace-pre-wrap">
          {logs || "Loading..."}
        </Text>
      </View>
    </ScrollView>
  );
}
