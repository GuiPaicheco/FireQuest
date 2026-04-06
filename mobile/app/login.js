import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import api from "../services/api";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function handleLogin() {
    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const response = await api.post("/auth/login", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      });

      const token =
        response.data.access_token ||
        response.data.data?.access_token;

      if (!token) {
        alert("Erro no login");
        return;
      }

      global.token = token;
      await AsyncStorage.setItem("token", token);
      api.defaults.headers.Authorization = `Bearer ${token}`;

      router.replace("/(tabs)");

    } catch (error) {
      alert("Login inválido");
    }
  }

  return (
    <View style={{
      flex: 1,
      backgroundColor: "#0a0a0f",
      justifyContent: "center",
      padding: 25
    }}>

      {/* LOGO / TÍTULO */}
      <Text style={{
        color: "#00fff7",
        fontSize: 32,
        fontWeight: "bold",
        marginBottom: 40,
        textAlign: "center",
        textShadowColor: "#00fff7",
        textShadowRadius: 15
      }}>
        FireQuest
      </Text>

      {/* INPUT USER */}
      <TextInput
        placeholder="Username"
        placeholderTextColor="#555"
        onChangeText={setUsername}
        style={{
          color: "white",
          borderWidth: 1,
          borderColor: "#00fff7",
          borderRadius: 12,
          padding: 15,
          marginBottom: 15
        }}
      />

      {/* INPUT PASSWORD */}
      <TextInput
        placeholder="Password"
        placeholderTextColor="#555"
        secureTextEntry
        onChangeText={setPassword}
        style={{
          color: "white",
          borderWidth: 1,
          borderColor: "#00fff7",
          borderRadius: 12,
          padding: 15,
          marginBottom: 25
        }}
      />

      {/* BOTÃO */}
      <TouchableOpacity
        onPress={handleLogin}
        style={{
          backgroundColor: "#00fff7",
          padding: 15,
          borderRadius: 12,
          alignItems: "center",
          shadowColor: "#00fff7",
          shadowOpacity: 0.7,
          shadowRadius: 10
        }}
      >
        <Text style={{
          color: "#0a0a0f",
          fontWeight: "bold",
          fontSize: 16
        }}>
          Entrar
        </Text>
      </TouchableOpacity>

    </View>
  );
}