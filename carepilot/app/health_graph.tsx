import React, { useState, useEffect } from "react";
import { View, Text, TouchableOpacity, Image, TextInput, Button, ScrollView } from "react-native";
import api from "../api";

export default function HealthScreen() {
  const [selected, setSelected] = useState("weight");
  const [imageUri, setImageUri] = useState(null);
  const [value, setValue] = useState("");
  const [date, setDate] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const options = [
    { key: "weight", label: "Body Weight" },
    { key: "sugar", label: "Blood Sugar" },
    { key: "pressure", label: "Blood Pressure" },
  ];

  const placeholders = {
    weight: "Enter weight in kg (e.g. 72)",
    sugar: "Enter blood sugar in mg/dL (e.g. 110)",
    pressure: "Enter systolic/diastolic (e.g. 120/80)",
  };

  const loadImage = () => {
    const base = api.defaults.baseURL;
    const uri = `${base}health-plot/?type=${selected}&t=${Date.now()}`;
    setImageUri(uri);
  };

  useEffect(() => {
    loadImage();
  }, [selected]);

  const handleTypeChange = (key) => {
    setSelected(key);
    setIsSubmitting(false);
    setValue("");
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);

    await api.post("/health-plot/", {
      type: selected,
      value,
      date,
    });

    alert("Record added successfully");
    setValue("");
    setDate("");
    loadImage();
  };

  return (
    <ScrollView className="flex-1 bg-white p-4">
      <View className="flex-row justify-around mb-4">
        {options.map(opt => (
          <TouchableOpacity
            key={opt.key}
            onPress={() => handleTypeChange(opt.key)}
            className={`px-4 py-2 rounded-xl ${
              selected === opt.key ? "bg-blue-600" : "bg-gray-200"
            }`}
          >
            <Text
              className={`${
                selected === opt.key ? "text-white" : "text-black"
              }`}
            >
              {opt.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {imageUri && (
        <Image
          source={{ uri: imageUri }}
          className="w-full h-64 rounded-xl border"
          resizeMode="contain"
        />
      )}

      <View className="mt-6">
        <Text className="text-lg font-semibold mb-3">
          Add {options.find(o => o.key === selected)?.label}
        </Text>

        <TextInput
          placeholder={placeholders[selected]}
          value={value}
          onChangeText={setValue}
          className="border rounded-lg p-3 mb-3"
        />

        <TextInput
          placeholder="Enter date (YYYY-MM-DD)"
          value={date}
          onChangeText={setDate}
          className="border rounded-lg p-3 mb-3"
        />

        <Button title="Submit" onPress={handleSubmit} disabled={isSubmitting} />
      </View>
    </ScrollView>
  );
}
