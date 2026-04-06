import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: "#0a0a0f",
          borderTopColor: "#00fff7"
        },
        tabBarActiveTintColor: "#00fff7",
        tabBarInactiveTintColor: "#555"
      }}
    >

      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => (
            <Ionicons name="home" size={22} color={color} />
          ),
        }}
      />

      <Tabs.Screen
        name="missions"
        options={{
          title: "Missões",
          tabBarIcon: ({ color }) => (
            <Ionicons name="flash" size={22} color={color} />
          ),
        }}
      />

      <Tabs.Screen
        name="ranking"
        options={{
          title: "Ranking",
          tabBarIcon: ({ color }) => (
            <Ionicons name="trophy" size={22} color={color} />
          ),
        }}
      />

      <Tabs.Screen
        name="profile"
        options={{
          title: "Perfil",
          tabBarIcon: ({ color }) => (
            <Ionicons name="person" size={22} color={color} />
          ),
        }}
      />

    </Tabs>
  );
}