import { Action } from "~/model/agentbody/Action";
import { ExperienceActionConsequence } from "~/model/experience/ExperienceActionConsequence";
import { ExperienceState } from "~/model/experience/ExperienceState";

describe('ExperienceActionConsequence', () => {
  describe('constructor', () => {
    test('should record action by value.', () => {
      const action = new Action('forward');
      expect(action.name).toBe('forward');

      const exacque = new ExperienceActionConsequence(action);

      action.name = 'back';

      const exacqueAction = exacque.action;

      expect(action.name).toBe('back');
      expect(exacqueAction.name).toBe('forward');
    });
  });

  describe('getters', () => {
    test('should return action by value.', () => {
      const action = new Action('forward');
      const exacque = new ExperienceActionConsequence(action);
      const exacqueAction1 = exacque.action;
      const exacqueAction2 = exacque.action;

      exacqueAction1.name = 'back';

      expect(exacqueAction1.name).toBe('back');
      expect(exacqueAction2.name).toBe('forward');
    });
  });

  describe('consequences', () => {
    let action: Action;
    let exacque: ExperienceActionConsequence;

    beforeEach(() => {
      action = new Action('forward');
      exacque = new ExperienceActionConsequence(action);
    });

    test('should initially know of no consequences.', () => {
      expect([...exacque.consequences]).toHaveLength(0);
    });

    test('should record a consequence.', () => {
      const exst = new ExperienceState({'alpha': true});
      exacque.recordConsequence(exst);
      expect([...exacque.consequences]).toHaveLength(1);
      for (let csq of exacque.consequences) {
        expect(csq.count).toBe(1);
        const eslt = csq.state.getStatelet('alpha');
        expect(eslt).not.toBeNull();
      }
    });

    test('should record equal existing consequences.', () => {
      const exst1 = new ExperienceState({'alpha': true});
      const exst2 = new ExperienceState({'alpha': true});
      exacque.recordConsequence(exst1);
      exacque.recordConsequence(exst2);
      expect([...exacque.consequences]).toHaveLength(1);
      for (let csq of exacque.consequences) {
        expect(csq.count).toBe(2);
        const eslt = csq.state.getStatelet('alpha');
        expect(eslt).not.toBeNull();
      }
    });

    test('should count matching consequences and add new.', () => {
      const exst1 = new ExperienceState({'alpha': true, 'beta': true});
      const exst2 = new ExperienceState({'alpha': true});
      exacque.recordConsequence(exst1);
      exacque.recordConsequence(exst2);

      const csqs = [...exacque.consequences];
      expect(csqs).toHaveLength(2);

      expect(csqs[0].count).toBe(2);
      expect(csqs[0].state.getStatelet('alpha')).not.toBeNull();
      expect(csqs[0].state.getStatelet('beta')).not.toBeNull();

      expect(csqs[1].count).toBe(1);
      expect(csqs[1].state.getStatelet('alpha')).not.toBeNull();
      expect(csqs[1].state.getStatelet('beta')).toBeNull();
    });

    test('should return consequence states by value.', () => {
      const action = new Action('forward');
      const exacque = new ExperienceActionConsequence(action);
      const exst = new ExperienceState({'alpha': true});
      exacque.recordConsequence(exst);

      const csq = [...exacque.consequences][0];
      expect(csq.state.getStatelet('alpha')).not.toBeNull();
      expect(csq.state.getStatelet('beta')).toBeNull();

      csq.state.setStatelet('beta');

      const csq2 = [...exacque.consequences][0];

      expect(csq.state.getStatelet('beta')).not.toBeNull();
      expect(csq2.state.getStatelet('beta')).toBeNull();
    });


  });
});
