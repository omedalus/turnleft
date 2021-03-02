import { Action } from "~/model/agentbody/Action";
import { ExperienceState } from "~/model/experience/ExperienceState";
import { ExperienceTableRow } from "~/model/experience/ExperienceTableRow";

describe('ExperienceTableRow', () => {
  describe('constructor', () => {
    test('should instantiate from an experience state by value.', () => {
      const exst = new ExperienceState({'alpha': true});
      const row = new ExperienceTableRow(exst);

      expect(exst.getStatelet('alpha')).not.toBeNull();
      expect(row.stateFrom.getStatelet('alpha')).not.toBeNull();

      expect(exst.getStatelet('beta')).toBeNull();
      expect(row.stateFrom.getStatelet('beta')).toBeNull();

      exst.setStatelet('beta');

      expect(exst.getStatelet('beta')).not.toBeNull();
      expect(row.stateFrom.getStatelet('beta')).toBeNull();
    });
  });

  describe('getters', () => {
    test('should retrieve stateFrom by value.', () => {
      const row = new ExperienceTableRow(new ExperienceState({'alpha': true}));
      const exst = row.stateFrom;

      expect(exst.getStatelet('alpha')).not.toBeNull();
      expect(exst.getStatelet('beta')).toBeNull();

      exst.setStatelet('beta');

      expect(exst.getStatelet('alpha')).not.toBeNull();
      expect(exst.getStatelet('beta')).not.toBeNull();

      expect(row.stateFrom.getStatelet('alpha')).not.toBeNull();
      expect(row.stateFrom.getStatelet('beta')).toBeNull();
    });
  });

  describe('recording and recalling actions', () => {
    // We're going to use a very simple toy problem involving entering a house.
    // You're standing on a porch, facing the house's front door.
    // If you go forward, you'll enter the house (if the door is open).
    // If you go backward, you'll end up back on the walkway leading up to the porch.
    let exstPorch: ExperienceState;
    let exstFoyer: ExperienceState;
    let exstWalkway: ExperienceState;
    let actForward: Action;
    let actBackward: Action;
    let row: ExperienceTableRow;

    beforeEach(() => {
      exstPorch = new ExperienceState({'onPorch': true, 'inFoyer': false, 'onWalkway': false});
      exstFoyer = new ExperienceState({'onPorch': false, 'inFoyer': true, 'onWalkway': false});
      exstWalkway = new ExperienceState({'onPorch': false, 'inFoyer': false, 'onWalkway': true});
      actForward = new Action('forward');
      actBackward = new Action('backward');
      row = new ExperienceTableRow(exstPorch);
    });

    test('should record and then recall an action with consequence.', () => {
      row.recordAction(actForward, exstFoyer);

      // Look up with a new equal action, so we make sure we're looking up by value
      // and not by object pointer.
      const exaque = row.lookupAction(new Action('forward'));
      expect(exaque.action.name).toBe('forward');
      const consequences = [...exaque.consequences];
      expect(consequences).toHaveLength(1);
      expect(consequences[0].count).toBe(1);
      expect(consequences[0].state.equals(exstFoyer)).toBeTruthy();
    });

    test('should record and then recall multiple actions, each with one consequence.', () => {
      row.recordAction(actForward, exstFoyer);
      row.recordAction(actBackward, exstWalkway);

      const exaqueFwd = row.lookupAction(new Action('forward'));
      expect(exaqueFwd.action.name).toBe('forward');
      const consequencesFwd = [...exaqueFwd.consequences];
      expect(consequencesFwd).toHaveLength(1);
      expect(consequencesFwd[0].count).toBe(1);
      expect(consequencesFwd[0].state.equals(exstFoyer)).toBeTruthy();

      const exaqueBack = row.lookupAction(new Action('backward'));
      expect(exaqueBack.action.name).toBe('backward');
      const consequencesBack = [...exaqueBack.consequences];
      expect(consequencesBack).toHaveLength(1);
      expect(consequencesBack[0].count).toBe(1);
      expect(consequencesBack[0].state.equals(exstWalkway)).toBeTruthy();
    });

    test('should record and then recall multiple actions, some with multiple consequence.', () => {
      // Walking forward COULD result in entering the foyer, or it could just result
      // in still being on the porch if the door is closed.
      row.recordAction(actForward, exstFoyer);
      row.recordAction(actForward, exstPorch);
      row.recordAction(actBackward, exstWalkway);

      const exaqueFwd = row.lookupAction(new Action('forward'));
      expect(exaqueFwd.action.name).toBe('forward');
      const consequencesFwd = [...exaqueFwd.consequences];
      expect(consequencesFwd).toHaveLength(2);
      expect(consequencesFwd[0].count).toBe(1);
      expect(consequencesFwd[0].state.equals(exstFoyer)).toBeTruthy();
      expect(consequencesFwd[1].count).toBe(1);
      expect(consequencesFwd[1].state.equals(exstPorch)).toBeTruthy();

      const exaqueBack = row.lookupAction(new Action('backward'));
      expect(exaqueBack.action.name).toBe('backward');
      const consequencesBack = [...exaqueBack.consequences];
      expect(consequencesBack).toHaveLength(1);
      expect(consequencesBack[0].count).toBe(1);
      expect(consequencesBack[0].state.equals(exstWalkway)).toBeTruthy();
    });


  });
});
