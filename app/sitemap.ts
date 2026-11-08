import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["/", "/politica-de-privacidade/", "/termos-de-uso/"].map((p) => ({
    url: `${SITE_URL}${p}`,
    changeFrequency: "monthly",
    priority: p === "/" ? 1 : 0.3,
  }));
}
