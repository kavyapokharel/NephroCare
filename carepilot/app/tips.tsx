import { useEffect, useState } from "react";
import { View, Text, ScrollView } from "react-native";

// Typewriter effect for one message
function useTypewriterMessage(message: string, start: boolean, speed = 15) {
  const [output, setOutput] = useState("");

  useEffect(() => {
    if (!start) return;

    let i = 0;
    const interval = setInterval(() => {
      setOutput(message.slice(0, i));
      i++;
      if (i > message.length) clearInterval(interval);
    }, speed);

    return () => clearInterval(interval);
  }, [start]);

  return output;
}

export default function Tips() {
  // Chat-style messages (general but feels personalized)
  const messages = [
    "👋 Hi there! I prepared some health guidance that’s helpful for people managing diabetes, CKD, blood pressure, or other chronic conditions.",

    "🫁 Try to keep a steady routine of light daily movement—such as walking for 15–25 minutes. It helps with blood sugar, blood pressure, and kidney/heart load.",

    "🥗 Choose meals with more vegetables, whole grains, and lean protein. Reducing salty and heavily processed foods supports the kidneys, heart, and blood pressure.",

    "💧 Hydration matters. Drink water consistently unless your doctor advised fluid restriction (common in CKD).",

    "🫀 Try slow deep breathing for 2–3 minutes daily. It helps reduce stress, stabilize BP, and protect long-term heart health.",

    "💊 If you're taking medications like BP meds, sugar control meds, or kidney-protective meds, try taking them at the same time each day.",

    "📈 Keep an eye on signs like swelling, unusual tiredness, dizziness, or sudden weight changes. These can be early signals your body gives when something needs attention.",

    "👍 Small, steady habits can make a huge difference — and you’re doing great by taking steps to stay informed!"
  ];

  // Track which message is currently animating
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  // Hold typewritten outputs for each message
  const typedOutputs = messages.map((msg, index) =>
    useTypewriterMessage(msg, currentMessageIndex === index)
  );

  // When a message finishes typing, trigger the next
  useEffect(() => {
    if (currentMessageIndex >= messages.length) return;

    const message = messages[currentMessageIndex];

    const timeout = setTimeout(() => {
      setCurrentMessageIndex((prev) => prev + 1);
    }, message.length * 15 + 600); // timing based on text length

    return () => clearTimeout(timeout);
  }, [currentMessageIndex]);

  return (
    <ScrollView className="flex-1 bg-gray-100 p-4">
      <Text className="text-center text-2xl font-bold text-blue-700 mb-6">
        Health Tips For You
      </Text>

      {typedOutputs.map((text, index) => {
        if (index > currentMessageIndex) return null; // Don’t show future msgs yet

        return (
          <View
            key={index}
            className="bg-white rounded-xl p-4 mb-4 shadow-md w-[90%] self-start"
          >
            <Text className="text-gray-900 text-lg leading-relaxed whitespace-pre-line">
              {text}
            </Text>
          </View>
        );
      })}
    </ScrollView>
  );
}
