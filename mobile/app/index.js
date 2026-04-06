import { useEffect, useState } from "react";
import { Redirect } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import api from "../services/api";

export default function Index() {
  const [loading, setLoading] = useState(true);
  const [isLogged, setIsLogged] = useState(false);

  useEffect(() => {
    async function checkLogin() {
      const token = await AsyncStorage.getItem("token");

      if (token) {
        global.token = token;
        api.defaults.headers.Authorization = `Bearer ${token}`;
        setIsLogged(true);
      }

      setLoading(false);
    }

    checkLogin();
  }, []);

  if (loading) return null;

  return isLogged ? <Redirect href="/(tabs)" /> : <Redirect href="/login" />;
}