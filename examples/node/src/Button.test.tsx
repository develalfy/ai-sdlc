import "@testing-library/jest-dom/vitest";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("renders with the supplied label as its accessible name", () => {
    render(<Button label="Save" />);
    expect(screen.getByRole("button", { name: "Save" })).toBeInTheDocument();
  });

  it("applies the variant class for variant=secondary", () => {
    render(<Button label="Cancel" variant="secondary" />);
    const btn = screen.getByRole("button", { name: "Cancel" });
    expect(btn).toHaveClass("btn", "btn--secondary");
  });

  it("invokes onClick exactly once per click", () => {
    const handleClick = vi.fn();
    render(<Button label="Go" onClick={handleClick} />);
    fireEvent.click(screen.getByRole("button", { name: "Go" }));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("defaults to the primary variant when variant is omitted", () => {
    render(<Button label="OK" />);
    expect(screen.getByRole("button", { name: "OK" })).toHaveClass("btn--primary");
  });
});