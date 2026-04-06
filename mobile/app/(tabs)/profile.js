import { View, Text, TouchableOpacity } from "react-native";
import { useEffect, useState, useCallback } from "react";
import { useFocusEffect } from "expo-router";
import api from "../../services/api";
import { useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  async function loadUser() {
    try {
      const response = await api.get("/users/me");

      if (response.data.success) {
        setUser(response.data.data);
      }

    } catch (error) {
      console.log("ERRO USER:", error);

      if (error.response) {
        alert("Erro: " + JSON.stringify(error.response.data));
      } else {
        alert("Erro de conexão");
      }
    }
  }

  async function logout() {
    await AsyncStorage.removeItem("token");
    global.token = null;
    router.replace("/login");
    }

    useFocusEffect(
    useCallback(() => {
        loadUser();
    }, [])
    );

  return (
    <View style={{
      flex: 1,
      backgroundColor: "#0a0a0f",
      justifyContent: "center",
      alignItems: "center",
      padding: 20
    }}>
      {user && (
        <View style={{
          width: "100%",
          alignItems: "center"
        }}>

          {/* USERNAME */}
          <Text style={{
            color: "#00fff7",
            fontSize: 28,
            fontWeight: "bold",
            textShadowColor: "#00fff7",
            textShadowOffset: { width: 0, height: 0 },
            textShadowRadius: 10
          }}>
            {user.username}
          </Text>

          {/* CARD */}
          <View style={{
            width: "100%",
            marginTop: 30,
            padding: 20,
            borderRadius: 20,
            backgroundColor: "#12121a",
            borderWidth: 1,
            borderColor: "#00fff7",
            shadowColor: "#00fff7",
            shadowOpacity: 0.3,
            shadowRadius: 20
          }}>

            {/* XP TEXT */}
            <Text style={{
              color: "white",
              marginBottom: 10,
              fontSize: 16
            }}>
              XP: {user.xp}
            </Text>

            {/* PROGRESS BAR */}
            <View style={{
              height: 20,
              backgroundColor: "#1a1a2e",
              borderRadius: 10,
              overflow: "hidden"
            }}>
              <View style={{
                width: `${(user.xp % 100)}%`,
                height: "100%",
                backgroundColor: "#00fff7",
                shadowColor: "#00fff7",
                shadowOpacity: 0.8,
                shadowRadius: 10
              }} />
            </View>

            {/* LEVEL */}
            <Text style={{
              color: "#00fff7",
              marginTop: 10,
              fontSize: 14
            }}>
              Nível {Math.floor(user.xp / 100)}
            </Text>

          </View>

          {/* BOTÃO */}
          <TouchableOpacity
            onPress={() => router.push("/missions")}
            style={{
              marginTop: 30,
              backgroundColor: "#00fff7",
              paddingVertical: 15,
              paddingHorizontal: 30,
              borderRadius: 15,
              shadowColor: "#00fff7",
              shadowOpacity: 0.6,
              shadowRadius: 15
            }}
          >
            <Text style={{
              color: "#0a0a0f",
              fontWeight: "bold",
              fontSize: 16
            }}>
              Ver Missões
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => router.push("/ranking")}
            style={{
                marginTop: 15,
                backgroundColor: "#1a1a2e",
                paddingVertical: 15,
                paddingHorizontal: 30,
                borderRadius: 15
            }}
            >
            <Text style={{
                color: "#00fff7",
                fontWeight: "bold"
            }}>
                Ver Ranking
            </Text>
            </TouchableOpacity>

        </View>
      )}
    </View>
  );
}