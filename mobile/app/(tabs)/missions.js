import { View, Text, FlatList, Button } from "react-native";
import { useEffect, useState } from "react";
import api from "../../services/api";
import { useFocusEffect } from "expo-router";
import { useCallback } from "react";

export default function Missions() {
  const [missions, setMissions] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  async function loadMissions() {
    try {
        setRefreshing(true);

        const response = await api.get("/missions/pending", {
        headers: {
            Authorization: `Bearer ${global.token}`
        }
        });

        if (response.data.success) {
        setMissions(response.data.data);
        }

    } catch (error) {
        console.log(error);
    } finally {
        setRefreshing(false);
    }
    }

    useFocusEffect(
    useCallback(() => {
        loadMissions();
    }, [])
    );

  return (
    <View style={{
      flex: 1,
      backgroundColor: "#0a0a0f",
      padding: 20
    }}>
      <Text style={{ color: "#00eaff", fontSize: 22, marginBottom: 20 }}>
        Missões
      </Text>

      <FlatList
        data={missions}
        refreshing={refreshing}
        onRefresh={loadMissions}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
            <View style={{
                borderColor: "#00eaff",
                borderWidth: 1,
                padding: 10,
                marginBottom: 10
            }}>
                <Text style={{ color: "white" }}>{item.title}</Text>
                <Text style={{ color: "#00eaff" }}>XP: {item.xp}</Text>

                <Button
                title="Concluir"
                onPress={() => completeMission(item.id)}
                />
            </View>
            )}
      />
    </View>
  );

  async function completeMission(id) {
  try {
    await api.put(`/missions/${id}/complete`);

    alert("Missão concluída 🚀");

    loadMissions(); // 🔥 atualiza lista

  } catch (error) {
    console.log(error);

    if (error.response) {
      alert(JSON.stringify(error.response.data));
    } else {
      alert("Erro ao concluir missão");
    }
  }
}
}