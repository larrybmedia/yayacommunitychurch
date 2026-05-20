import { SafeAreaView } from "react-native";
import { WebView } from "react-native-webview";

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <WebView source={{ uri: "https://YOUR-FLASK-APP-URL" }} />
    </SafeAreaView>
  );
}