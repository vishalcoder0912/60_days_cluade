import type {Config} from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#fdfbf7",
        ink: "#2d2d2d",
        muted: "#e5e0d8",
        marker: "#ff4d4d",
        pen: "#2d5da1",
        note: "#fff9c4",
      },
      fontFamily: {
        heading: ["Kalam", "cursive"],
        body: ["Patrick Hand", "cursive"],
      },
      borderRadius: {
        wobbly: "255px 18px 225px 20px / 18px 225px 20px 255px",
        wobblyMd: "35px 18px 32px 14px / 16px 36px 18px 30px",
      },
      boxShadow: {
        hard: "4px 4px 0 0 #2d2d2d",
        hardLg: "8px 8px 0 0 #2d2d2d",
        paper: "4px 4px 0 0 rgba(45, 45, 45, 0.16)",
      },
      keyframes: {
        bob: {
          "0%, 100%": {transform: "translateY(0) rotate(-2deg)"},
          "50%": {transform: "translateY(-8px) rotate(1deg)"},
        },
      },
      animation: {
        bob: "bob 3s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
