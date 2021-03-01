import { StateMemo } from "./StateMemo";

export class Plan
{
  private Plan()
  {

  }

  public static devise(initialStateGenerator: any, params: any) : Plan {
    const plan = new Plan();
    const memo = new StateMemo();
    return plan;
  }
};
