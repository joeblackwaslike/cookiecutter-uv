import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: "category",
      label: "Getting Started",
      items: ["intro", "installation", "quickstart"],
    },
    {
      type: "category",
      label: "User Guide",
      items: ["usage", "configuration"],
    },
    {
      type: "category",
      label: "Contributing",
      items: ["contributing"],
    },
  ],
};

export default sidebars;
