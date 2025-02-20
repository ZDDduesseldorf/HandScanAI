import { Button, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'solid' | 'outlined';
  sx?: object;
}

/**
 * A wide button with two variations: solid (which is default) and outlined.
 *
 * @param onClick Action that is executed when the button is clicked
 * @param children Content of the button
 * @param variant Variation of the button, default: "solid"
 * @returns Button component
 */
export default function Wide({ onClick, children, variant = 'solid', sx }: Props) {
  /**
   * Styling for a mui <button> component that adds a wide (min-width 360ox)
   * button and adds a hover effect. This is for the solid variant.
   */
  const Wide = styled(Button)`
    background-color: var(--primary);
    color: white;
    font-family: 'Delius Unicase', cursive;
    padding: 0.5em 1em;
    font-size: 1.5em;
    height: 2.5em;
    transition: background-color 0.3s;
    border-radius: 0;
    min-width: 360px;
    text-transform: none;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  /**
   * Styling for a mui <button> component that adds a wide (min-width 360ox)
   * button and adds a hover effect. This is for the outlined variant.
   */
  const WideOutlined = styled(Button)`
    border: 2px solid var(--primary);
    color: var(--primary);
    font-family: 'Delius Unicase', cursive;
    padding: 0.5em 1em;
    font-size: 1.5em;
    height: 2.5em;
    transition: background-color 0.3s;
    border-radius: 0;
    text-transform: none;
    min-width: 360px;
    background-color: transparent;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return variant == 'outlined' ? (
    <WideOutlined onClick={onClick} sx={sx}>{children}</WideOutlined>
  ) : (
    <Wide onClick={onClick} sx={sx}>{children}</Wide>
  );
}
