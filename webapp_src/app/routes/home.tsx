import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export default function Home() {
  return (
    <div>
      <title>Partner Chat</title>
      <meta name="description" content="A place to speak to an AI of your choosing" />
      <Welcome />
    </div>
  )
}
