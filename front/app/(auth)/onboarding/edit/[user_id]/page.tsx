import { OnBoardingEdit } from "@/shared/components/onboarding/onboarding-edit";

interface Props {
  params: Promise<{ user_id: string }>;
}

export default async function EditProfilePage({ params }: Props) {
  const { user_id } = await params;

  return <OnBoardingEdit isEditing={true} userId={user_id} />;
}
