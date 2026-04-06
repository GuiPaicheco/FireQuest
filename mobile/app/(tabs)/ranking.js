import { View, Text, FlatList } from "react-native";
import { useEffect, useState } from "react";
import api from "../../services/api";

export default function Ranking() {
  const [ranking, setRanking] = useState([]);

  async function loadRanking() {
    try {
      const response = await api.get("/users/ranking");

      if (response.data.success) {
        setRanking(response.data.data);
      }

    } catch (error) {
      console.log(error);
      alert("Erro ao carregar ranking");
    }
  }

  useEffect(() => {
    loadRanking();
  }, []);

  return (
    <View style={{
      flex: 1,
      backgroundColor: "#0a0a0f",
      padding: 20
    }}>
      <Text style={{
        color: "#00fff7",
        fontSize: 22,
        marginBottom: 20
      }}>
        Ranking
      </Text>

      <FlatList
        data={ranking}
        keyExtractor={(item) => item.position.toString()}
        renderItem={({ item }) => (
          <View style={{
            borderBottomWidth: 1,
            borderBottomColor: "#1a1a2e",
            paddingVertical: 10
          }}>
            <Text style={{ color: "white" }}>
              #{item.position} - {item.username}
            </Text>

            <Text style={{ color: "#00fff7" }}>
              XP: {item.xp}
            </Text>
          </View>
        )}
      />
    </View>
  );
}