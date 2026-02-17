import React, { useState } from "react";
import {
  View, Text, TextInput, TouchableOpacity, FlatList,
  StatusBar, Alert
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Picker } from "@react-native-picker/picker";
import api from "../api";

export default function Consultation() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Please describe any problems you want to go over during consultation." }
  ]);

  const [input, setInput] = useState("");
  const [step, setStep] = useState("symptom");
  const [isDisabled, setIsDisabled] = useState(false);

  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [availableDates, setAvailableDates] = useState([]);

  const [symptomMessage, setSymptomMessage] = useState("");

  const sendMessage = async () => {
    if (!input.trim() || isDisabled) return;

    const userText = input;
    setSymptomMessage(input)
    setInput("");
    setMessages(prev => [...prev, { sender: "user", text: userText }]);

    try {
      const res = await api.post("consultation/", {
        step: step,
        message: userText,
      });

      handleBackendResponse(res.data);

    } catch (e) {
      Alert.alert("Error", JSON.stringify(e));
    }
  };

  const submitDateRange = async () => {
    if (!fromDate || !toDate) {
      Alert.alert("Missing", "Please select both From Date and To Date.");
      return;
    }

    setMessages(prev => [
      ...prev,
      { sender: "user", text: `From: ${fromDate} → To: ${toDate}` }
    ]);

    try {
      const res = await api.post("consultation/", {
        step: "choose_date",
        from_date: fromDate,
        to_date: toDate,
      });

      handleBackendResponse(res.data);

    } catch (e) {
      Alert.alert("Error", JSON.stringify(e));
    }
  };

  const selectFinalDate = async (date) => {
    setMessages(prev => [...prev, { sender: "user", text: `Selected: ${date}` }]);

    try {
      const res = await api.post("consultation/", {
        step: "confirm",
        selected_date: date,
        message: symptomMessage,
      });

      handleBackendResponse(res.data);
    } catch (e) {
      Alert.alert("Error", JSON.stringify(e));
    }
  };

  const handleBackendResponse = (data) => {
    if (data.message) {
      setMessages(prev => [...prev, { sender: "bot", text: data.message }]);
    }

    if (data.step === "choose_date" && !data.dates) {
      setStep("choose_date");
      return;
    }

    if (data.step === "choose_date" && data.dates) {
      setAvailableDates(data.dates);
      setStep("select_final_date");
      return;
    }

    if (data.step === "done") {
      setIsDisabled(true);
      setStep("done");
      return;
    }
  };

  const renderMessage = ({ item }) => (
    <View
      className={`px-4 py-3 m-2 mx-4 rounded-2xl max-w-[80%] ${
        item.sender === "user"
          ? "self-end bg-blue-600"
          : "self-start bg-gray-200"
      }`}
    >
      <Text
        className={`text-lg leading-6 ${
          item.sender === "user" ? "text-white" : "text-black"
        }`}
      >
        {item.text}
      </Text>
    </View>
  );

  const renderAvailableDates = () => (
    <View className="p-3">
      {availableDates.map((d, i) => (
        <TouchableOpacity
          key={i}
          className="p-3 bg-gray-200 rounded-xl m-1"
          onPress={() => selectFinalDate(d)}
        >
          <Text className="text-lg">{d}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  return (
    <SafeAreaView className="flex-1 bg-white">
      <StatusBar />

      <FlatList
        data={messages}
        keyExtractor={(_, i) => i.toString()}
        renderItem={renderMessage}
        contentContainerStyle={{ paddingTop: 12, paddingBottom: 20 }}
      />

      {step === "choose_date" && (
        <View className="p-4">
          <Text className="text-lg mb-2">Select From Date:</Text>
          <Picker selectedValue={fromDate} onValueChange={(v) => setFromDate(v)}>
            <Picker.Item label="Choose date..." value="" />
            <Picker.Item label="2025-11-15" value="2025-11-15" />
            <Picker.Item label="2025-11-20" value="2025-11-20" />
            <Picker.Item label="2025-11-25" value="2025-11-25" />
          </Picker>

          <Text className="text-lg my-2">Select To Date:</Text>
          <Picker selectedValue={toDate} onValueChange={(v) => setToDate(v)}>
            <Picker.Item label="Choose date..." value="" />
            <Picker.Item label="2025-11-20" value="2025-11-20" />
            <Picker.Item label="2025-11-25" value="2025-11-25" />
            <Picker.Item label="2025-11-30" value="2025-11-30" />
          </Picker>

          <TouchableOpacity
            className="bg-blue-600 p-3 mt-3 rounded-xl"
            onPress={submitDateRange}
          >
            <Text className="text-white text-lg text-center">Submit</Text>
          </TouchableOpacity>
        </View>
      )}

      {step === "select_final_date" && renderAvailableDates()}

      {step === "symptom" && (
        <View className="flex-row items-center m-4 p-2">
          <TextInput
            className="flex-1 border border-gray-300 rounded-xl p-3 mr-2 text-lg"
            value={input}
            onChangeText={setInput}
            placeholder="Type your message..."
            placeholderTextColor="#888"
            editable={!isDisabled}
          />

          <TouchableOpacity
            onPress={sendMessage}
            disabled={isDisabled}
            className={`px-5 py-3 rounded-xl ${
              isDisabled ? "bg-gray-300" : "bg-blue-600"
            }`}
          >
            <Text className="text-white font-bold text-lg">Send</Text>
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}
